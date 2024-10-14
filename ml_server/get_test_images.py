"""
This script saves a specified number of random test images from the Fashion MNIST dataset to a directory named 'test_images'.
Usage:
    python get_test_images.py [num_images]
Arguments:
    num_images (int, optional): The number of images to save. Defaults to 10.
Example:
    python get_test_images.py 5
This will save 5 random test images from the Fashion MNIST dataset into the 'test_images' directory.
"""
import os
import argparse
import numpy as np
from PIL import Image
from tensorflow.keras.datasets import fashion_mnist

def main(num_images):
    # Load the Fashion MNIST dataset
    (_, _), (test_images, test_labels) = fashion_mnist.load_data()

    # Ensure the 'test_images' directory exists
    os.makedirs('test_images', exist_ok=True)

    # Select num_images random indices from the test dataset
    if num_images > len(test_images):
        print(f"Requested number of images ({num_images}) exceeds the available test images ({len(test_images)}).")
        num_images = len(test_images)
        print(f"Proceeding with {num_images} images.")

    random_indices = np.random.choice(len(test_images), size=num_images, replace=False)

    # Save each selected image to the 'test_images' folder
    for idx, image_index in enumerate(random_indices):
        image = Image.fromarray(test_images[image_index])
        image_filename = f'test_image_{idx+1}.png'
        image.save(os.path.join('test_images', image_filename))
        print(f'Saved {image_filename}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Save random test images from the Fashion MNIST dataset.')
    parser.add_argument('num_images', type=int, nargs='?', default=10,
                        help='Number of images to save (default: 10)')
    args = parser.parse_args()
    main(args.num_images)
