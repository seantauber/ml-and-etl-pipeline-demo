import json
import numpy as np
import requests
import tensorflow as tf

# Load a sample image
(_, _), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
test_image = test_images[0]
test_image = test_image.astype(np.float32) / 255.0
test_image = test_image.reshape(1, 28, 28)

# Prepare the data for TensorFlow Serving
data = json.dumps({"instances": test_image.tolist()})

# Send the request
headers = {"content-type": "application/json"}
json_response = requests.post('http://localhost:8501/v1/models/mnist_model:predict', data=data, headers=headers)
predictions = json.loads(json_response.text)['predictions']
print("Predicted class:", np.argmax(predictions[0]))
