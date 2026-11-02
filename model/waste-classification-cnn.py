import tensorflow as tf
from PIL import Image
import numpy as np
import keras
import os
from keras.applications.mobilenet_v2 import preprocess_input

data_dir = "/Users/sajadeen/Desktop/GitHub/waste-reducing-app-hackathon/images/"
test_image = "/Users/sajadeen/Desktop/GitHub/waste-reducing-app-hackathon/test.png"

converted_count = 0
deleted_count = 0

for directory in os.listdir(data_dir):
  for file in os.listdir(os.path.join(data_dir, directory)):
    allowed_extensions = ["png", "jpg", "jpeg", "gif", "bmp"]
    change_needed = False
    for extension in allowed_extensions:
      if file.endswith(extension):
        break
      else:
        change_needed = True
    if change_needed:
      try:
        full_path = os.path.join(data_dir, directory, file)
        img = Image.open(full_path)
        saved_image = img.save(full_path.split(".")[0] + ".png", "PNG")
        converted_count += 1
        os.remove(full_path)
      except Exception as e:
        os.remove(full_path)
        deleted_count += 1

print(converted_count, "images converted to PNG.")
print (deleted_count, "corrupted images deleted.")
            
data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomRotation(0.1),
    keras.layers.RandomZoom(0.2),
    keras.layers.RandomFlip("vertical")
])

def preprocess(image, label):
    image = tf.cast(image, tf.float32)
    image = preprocess_input(image)
    return image, label

def augment(image, label):
    image = data_augmentation(image)
    return image, label

train_ds = keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    image_size=(256, 256),
    batch_size=32,
    seed=42
)

val_ds = keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    image_size=(256, 256),
    batch_size=32,
    seed=42
)

train_ds = train_ds.map(preprocess).map(augment).cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
val_ds = val_ds.map(preprocess).cache().prefetch(buffer_size=tf.data.AUTOTUNE)

base_model = keras.applications.MobileNetV2(input_shape=(256, 256, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(len(train_ds.class_names), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=6,
    restore_best_weights=True
)
model.fit(train_ds, validation_data=val_ds, epochs=40, callbacks=[early_stopping])

model.save("waste_classifier2.keras")

img = keras.utils.load_img(test_image, target_size=(256, 256))
img_array = keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)
img_array = preprocess_input(img_array)

predictions = model.predict(img_array)
highest_score = np.argmax(predictions)

print("Predicted class:", train_ds.class_names[highest_score])