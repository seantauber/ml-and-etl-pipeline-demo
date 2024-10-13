from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

def train_model():
    # Load the Fashion MNIST dataset inside the container
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

    # Normalize the images
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    # Reshape the images for the CNN
    train_images = train_images.reshape(-1, 28, 28, 1)
    test_images = test_images.reshape(-1, 28, 28, 1)

    # Define the model architecture
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax')  # 10 classes
    ])

    # Compile the model
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Train the model
    model.fit(train_images, train_labels, epochs=5, validation_data=(test_images, test_labels))

    # Save the model
    model.save('fashion_mnist_model.h5')

# Set up a route to train the model
@app.route('/train', methods=['POST'])
def train():
    try:
        train_model()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'Model trained and saved successfully'}), 200

# Load the model (this will be updated after training)
model = None

# Define class names
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Set up a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        if os.path.exists('fashion_mnist_model.h5'):
            model = keras.models.load_model('fashion_mnist_model.h5')
        else:
            return jsonify({'error': 'Model not found. Please train the model first.'}), 400

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    img_bytes = file.read()
    # Preprocess the image
    image = Image.open(io.BytesIO(img_bytes)).convert('L')
    image = image.resize((28, 28))
    image = np.array(image) / 255.0
    image = image.reshape(1, 28, 28, 1)
    # Make prediction
    predictions = model.predict(image)
    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))
    return jsonify({'class': predicted_class, 'confidence': confidence})

if __name__ == '__main__':
    if not os.path.exists('fashion_mnist_model.h5'):
        print("Training model...")
        train_model()
    app.run(host='0.0.0.0', port=5002)
