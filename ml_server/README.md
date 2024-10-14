# Fashion MNIST CNN Classifier

This project implements a Convolutional Neural Network (CNN) classifier for the Fashion MNIST dataset using TensorFlow and Flask. It provides a web server with endpoints for training the model and making predictions on new images.

## Quick Start

1. Start the service:
   ```
   docker-compose up --build
   ```

2. Run predictions:
   ```
   chmod +x run_predictions.sh
   ./run_predictions.sh
   ```

These steps will start the service, generate 10 test images, and run predictions on them.

## Table of Contents

- [Fashion MNIST CNN Classifier](#fashion-mnist-cnn-classifier)
  - [Quick Start](#quick-start)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Setup and Installation](#setup-and-installation)
  - [Usage](#usage)
    - [Training the Model](#training-the-model)
    - [Making Predictions](#making-predictions)
  - [Testing](#testing)
  - [API Endpoints](#api-endpoints)
  - [Docker Deployment](#docker-deployment)
  - [Troubleshooting](#troubleshooting)


## Project Structure

- `app.py`: Main Flask application with routes for training and prediction
- `Dockerfile`: Instructions for building the Docker image
- `docker-compose.yaml`: Docker Compose configuration for easy deployment
- `get_test_images.py`: Script to generate test images from the Fashion MNIST dataset
- `requirements.txt`: Python dependencies for the project
- `run_predictions.sh`: Bash script to test the prediction endpoint with multiple images

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- curl (for testing)
- 10GB Local storage for data

## Setup and Installation

1. Clone this repository:
   ```
   git clone [https://github.com/seantauber/ml-and-etl-pipeline-demo.git
   cd <project-directory>/ml_server
   ```

2. Build and start the Docker container:
   ```
   docker-compose up --build
   ```

   This will start the Flask server on `http://localhost:5002`.

## Usage

### Training the Model

The model will be automatically trained when you start the Docker container if no pre-trained model exists. To manually trigger training later:

```bash
curl -X POST http://localhost:5002/train
```

### Making Predictions

To make a prediction on a single image:

```bash
curl -X POST -F "file=@path/to/your/image.png" http://localhost:5002/predict
```

For example, to make a prediction on an image named `tshirt.png` located in your current directory, you can use the following command:

```bash
curl -X POST -F "file=@test_images/test_image_1.png" http://localhost:5002/predict
```

This will send the image to the server and return the predicted class.

There are 10 test images in `/test_images` that you can use to test.


Replace `path/to/your/image.png` with the actual path to your image file.

Using Postman:
1. Create a new POST request to `http://localhost:5002/predict`
2. In the "Body" tab, select "form-data"
3. Add a key named "file" and select "File" as the type
4. Upload your image file
5. Send the request

## Testing

1. Generate test images:
   ```
   python get_test_images.py [num_images]
   ```
   Replace `[num_images]` with the number of test images you want to generate (default is 10).

2. Run the prediction test script:
   ```
   chmod +x run_predictions.sh
   ./run_predictions.sh
   ```

   This script will send each generated test image to the prediction endpoint and display the results.

## API Endpoints

- `POST /train`: Train the model
- `POST /predict`: Predict the class of an uploaded image

## Docker Deployment

To deploy the application using Docker:

1. Ensure Docker and Docker Compose are installed on your system.
2. Navigate to the project directory.
3. Run:
   ```
   docker-compose up --build
   ```
4. The server will be available at `http://localhost:5002`.

To stop the container:
```
docker-compose down
```

## Troubleshooting

- If you encounter permission issues with `run_predictions.sh`, ensure it's executable:
  ```
  chmod +x run_predictions.sh
  ```
- If the server doesn't start, check Docker logs:
  ```
  docker-compose logs
  ```
- Ensure that the `test_images` directory exists and contains PNG files before running `run_predictions.sh`.

For any other issues, please check the application logs or open an issue in the project repository.