import tensorflow as tf
from PIL import Image
import numpy as np
import os

data_dir = "/Users/sajadeen/Desktop/GitHub/waste-reducing-app-hackathon/images/"
test_image = "/Users/sajadeen/Desktop/GitHub/waste-reducing-app-hackathon/test.png"

converted_count = 0
deleted_count = 0

for root, dirs, files in os.walk(data_dir):
  for file in files:
    if file.startswith("."):
      continue

    file_path = os.path.join(root, file)

    try:
      with Image.open(file_path) as img:
        if img.format == "WEBP":
          base, _ = os.path.splitext(file_path)
          new_path = base + ".png"
          img.save(new_path, "PNG")

          os.remove(file_path)

          converted_count += 1
        else:
          img.verify()

    except Exception as e:
      try:
        os.remove(file_path)
        deleted_count += 1
      except Exception as rm_err:
        print(f"Could not delete {file_path}: {rm_err}")

print(converted_count, "images converted from WEBP to PNG.")
print (deleted_count, "corrupted images deleted.")

class_names = [
  "batteries", "cans_all_types", "cermaic_product", "cofee_tea_bags", "coffee_tea_bags", "diapers", "e-waste", "egg_shells", "food_scraps", "glass_containers", "kitchen_waste", "paints", "paper_products", "pesticides", "plastic_bottles", "plastic_bags_wrappers", "sanitary_napkin", "stroform_product", "yard_trimmings"
]

img = tf.keras.utils.load_img(test_image, target_size=(256, 256))

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

num_classes = 18

architecture_blueprint = [
  (32, 3),
  (64, 3),
  (128, 3),
  (256, 3)
]

train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=42,
  image_size=(256, 256),
  batch_size=32
) 

val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=42,
  image_size=(256, 256),
  batch_size=32
)

layers_list = [tf.keras.layers.Input(shape=(256, 256, 3))]

for filters, num_layers in architecture_blueprint:
  for _ in range(num_layers):
    layers_list.append(tf.keras.layers.Conv2D(filters, (3, 3), activation='relu', padding="same"))
  if (filters > 32):
    layers_list.append(tf.keras.layers.MaxPool2D((2, 2), padding="same"))

layers_list.extend([
  tf.keras.layers.Flatten(),
  
  tf.keras.layers.Dense(512, activation='relu'),
  tf.keras.layers.Dropout(0.5),

  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dropout(0.3),

  tf.keras.layers.Dense(num_classes, activation='softmax')
])

model = tf.keras.Sequential(layers_list)

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=40,
)

model.save("waste_classifier_model.keras")

predictions = model.predict(img_array)

highest_score_index = np.argmax(predictions)

predicted_class = class_names[highest_score_index]

confidence = 100 * np.max(predictions)

print(f"Predicted class: {predicted_class} with confidence: {confidence:.2f}%")
