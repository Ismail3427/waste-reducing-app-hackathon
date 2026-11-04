import tensorflow as tf
from PIL import Image
import numpy as np
import keras
import os
from keras.applications import MobileNetV2

data_dir = "/Users/sajadeen/Desktop/GitHub/waste-reducing-app-hackathon/images/"
test_image = "/Users/sajadeen/Desktop/GitHub/waste-reducing-app-hackathon/test.png"

converted_count = 0
deleted_count = 0

for dir in os.listdir(data_dir):
    if dir == ".DS_Store":
        continue
    for file in os.listdir(os.path.join(data_dir, dir)):
        if file == ".DS_Store":
            continue
        allowed_exts = ["jpeg", "png", "gif", "bmp"]
        try:
            with Image.open(os.path.join(data_dir, dir, file)) as image_loaded:
                image_loaded.verify()

            with Image.open(os.path.join(data_dir, dir, file)) as image_loaded:
                acutal_ext = image_loaded.format.lower()
                if acutal_ext not in allowed_exts:
                    image_loaded.save(
                        os.path.join(data_dir, dir, file.split(".")[0] + ".png"),
                        "PNG",
                        icc_profile=None,
                    )
                    os.remove(os.path.join(data_dir, dir, file))
                    converted_count += 1
                    print(f"Converted {file} to PNG")
                    file = os.path.join(data_dir, dir, file.split(".")[0] + ".png")
                    if image_loaded.mode in ("RGBA", "P", "CMYK"):
                        image_loaded = image_loaded.convert("RGB")
                else:
                    image_loaded.save(
                        os.path.join(data_dir, dir, file),
                        image_loaded.format,
                        icc_profile=None,
                    )
        except Exception as e:
            os.remove(os.path.join(data_dir, dir, file))
            deleted_count += 1
            print(f"Deleted {file} due to error")

print(f"Converted: {converted_count}")
print(f"Deleted: {deleted_count}")

data_augmentation = keras.Sequential(
    [
        keras.layers.RandomFlip("horizontal"),
        keras.layers.RandomRotation(0.1),
        keras.layers.RandomZoom(0.2),
        keras.layers.RandomFlip("vertical"),
    ]
)

train_ds = keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    image_size=(224, 224),
    batch_size=32,
    seed=42,
)

val_ds = keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    image_size=(224, 224),
    batch_size=32,
    seed=42,
)

class_names = train_ds.class_names
num_classes = len(class_names)

base_model = MobileNetV2(
    input_shape=(224, 224, 3), include_top=False, weights="imagenet"
)

base_model.trainable = False

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

model = keras.Sequential(
    [
        data_augmentation,
        keras.layers.Lambda(
            lambda x: keras.applications.mobilenet_v2.preprocess_input(x)
        ),
        base_model,
        keras.layers.GlobalAveragePooling2D(),
        keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

model.compile(
    loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
)

model.fit(train_ds, validation_data=val_ds, epochs=15)

base_model.trainable = True

for layer in base_model.layers[:100]:
    layer.trainable = False

custom_omtimizer = keras.optimizers.Adam(learning_rate=1e-5)

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=custom_omtimizer,
    metrics=["accuracy"],
)

early_stopping = keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=5, restore_best_weights=True
)
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=40,
    callbacks=[early_stopping],
    initial_epoch=15,
)

model.save("waste_classification_model.keras")
