import tensorflow as tf
import keras
import numpy as np
import builtins

builtins.keras = keras

test_image = "/Users/ismail/Documents/GitHub/waste-reducing-app-hackathon/model-creation/test.png"
img = keras.utils.load_img(test_image, target_size=(224, 224))
img_array = keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)
img_array = keras.applications.mobilenet_v2.preprocess_input(img_array)

model = keras.models.load_model(
    "/Users/ismail/Documents/GitHub/waste-reducing-app-hackathon/model-creation/waste_classification_model.keras",
    custom_objects={
        "preprocess_input": keras.applications.mobilenet_v2.preprocess_input
    },
    safe_mode=False,
)

predictions = model.predict(img_array)

classes = [
    "batteries",
    "cans_all_type",
    "ceramic_product",
    "coffee_tea_bags",
    "diapers",
    "e-waste",
    "egg_shells",
    "food_scraps",
    "glass_containers",
    "kitchen_waste",
    "paints",
    "yard_trimmings",
]
num_classes = len(classes)

print("Predicted class:", classes[np.argmax(predictions)])
