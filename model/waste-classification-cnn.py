import tensorflow as tf
from PIL import Image
import numpy as np
import keras
import os

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
            if (acutal_ext not in allowed_exts):
              image_loaded.save(os.path.join(data_dir, dir, file.split(".")[0] + ".png"), "PNG", icc_profile=None)
              os.remove(os.path.join(data_dir, dir, file))
              converted_count += 1
              print(f"Converted {file} to PNG")
              file = os.path.join(data_dir, dir, file.split(".")[0] + ".png")
              if image_loaded.mode in ("RGBA", "P", "CMYK"):
                image_loaded = image_loaded.convert("RGB")
            else:
              image_loaded.save(os.path.join(data_dir, dir, file), image_loaded.format, icc_profile=None)
        except Exception as e:
          os.remove(os.path.join(data_dir, dir, file))
          deleted_count += 1
          print(f"Deleted {file} due to error")

print(f"Converted: {converted_count}")
print(f"Deleted: {deleted_count}")

data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomRotation(0.1),
    keras.layers.RandomZoom(0.2),
    keras.layers.RandomFlip("vertical")
])

train_ds = keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  image_size=(224, 224),
  batch_size=32,
  seed=42
)

val_ds = keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  image_size=(224, 224),
  batch_size=32,
  seed=42
)

class_names = train_ds.class_names
num_classes = len(class_names)

model = keras.Sequential([
  keras.layers.Rescaling(1./255, input_shape=(224, 224, 3)),
  
  data_augmentation,

  keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),

  keras.layers.MaxPooling2D((2, 2)),

  keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),

  keras.layers.MaxPooling2D((2, 2)),

  keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),

  keras.layers.MaxPooling2D((2, 2)),

  keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
  keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),

  keras.layers.MaxPooling2D((2, 2)),

  keras.layers.Flatten(),

  keras.layers.Dense(512, activation='relu'),
  keras.layers.Dropout(0.5),

  keras.layers.Dense(256, activation='relu'),
  keras.layers.Dropout(0.3),

  keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(train_ds, validation_data=val_ds, epochs=40)

model.save("waste_classifier.keras")

img = keras.utils.load_img(test_image, target_size=(224, 224))
img_array = keras.utils.img_to_array(img)

predictions = model.predict(img_array)

highest_score = np.argmax(predictions)

prediction = class_names[highest_score]

print(f"Predicted class: {prediction}")
