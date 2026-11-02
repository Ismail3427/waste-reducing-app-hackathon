import tensorflow as tf
from PIL import Image
import numpy as np
import keras
import os

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

print(converted_count, "images converted from WEBP to PNG.")
print (deleted_count, "corrupted images deleted.")

img = keras.utils.load_img(test_image, target_size=(256, 256))

img_array = keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

base_model = keras.applications.MobileNetV2(input_shape=(256, 256, 3), include_top=False, weights='imagenet')

base_model.trainable = False

train_ds = keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  image_size=(256, 256),
  batch_size=32,
  seed=42
)

class_names = train_ds.class_names
num_classes = len(class_names)

val_ds = keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  image_size=(256, 256),
  batch_size=32,
  seed=42
)

data_augmentation = keras.Sequential([
  keras.layers.RandomFlip("horizontal"),
  keras.layers.RandomRotation(0.1),
  keras.layers.RandomZoom(0.2),
  keras.layers.RandomFlip("vertical")
])

model = keras.Sequential([
  data_augmentation,

  keras.layers.Lambda(keras.applications.mobilenet_v2.preprocess_input, input_shape=(256, 256, 3)),
    
  base_model,

  keras.layers.GlobalAveragePooling2D(),
  keras.layers.Dropout(0.5),

  keras.layers.Dense(num_classes, activation='softmax')
])

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=6,
    restore_best_weights=True,
)

model.compile(
  optimizer='adam', 
  loss='sparse_categorical_crossentropy', 
              metrics=['accuracy'],
)

model.fit(train_ds, validation_data=val_ds, epochs=40, callbacks=[early_stopping])

model.save("waste_classifier2.keras")

img_array = keras.applications.mobilenet_v2.preprocess_input(img_array)

predictions = model.predict(img_array)
highest_score = np.argmax(predictions)

print(class_names[highest_score])
