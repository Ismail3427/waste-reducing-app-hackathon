import tensorflow as tf
import numpy as np

data_dir = "../images"
test_image = "../image.png"

class_names = [
  "batteries", "cans_all_types", "cermaic_product", "cofee_tea_bags", "coffee_tea_bags", "diapers", "e-waste", "egg_shells", "food_scraps", "glass_containers", "kitchen_waste", "paints", "paper_products", "pesticides", "plastic_bottles", "plastic_bags_wrappers", "sanitary_napkin", "stroform_product", "yard_trimmings"
]

img = tf.keras.utils.load_img(test_image, target_size=(150, 150))

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
  seed=123,
  image_size=(150, 150),
  batch_size=32
)

val_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(150, 150),
  batch_size=32
)

layers_list = [tf.keras.layers.Input(shape=(150, 150, 3))]

for filters, num_layers in architecture_blueprint:
  for _ in range(num_layers):
    layers_list.append(tf.keras.layers.Conv2D(filters, (3, 3), activation='relu', padding="same"))
    layers_list.append(tf.keras.layers.MaxPooling2D((2, 2)))
  layers_list.append(tf.keras.layers.MaxPool2D((2, 2)))

layers_list.extend([
  tf.keras.layers.Flatten(),
  
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dropout(0.5),

  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.3),

  tf.keras.layers.Dense(num_classes, activation='softmax')
])

model = tf.keras.Sequential(layers_list)

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=10
)

predictions = model.predict(img_array)

highest_score_index = np.argmax(predictions)

predicted_class = class_names[highest_score_index]

confidence = 100 * np.max(predictions)

print(f"Predicted class: {predicted_class} with confidence: {confidence:.2f}%")
