# This script iterates over all PNG files in the 'test_images' directory,
# sends each file to a local server for prediction via a POST request,
# and prints the server's response.
#
# Usage:
#   ./run_predictions.sh
#
# Requirements:
#   - The 'test_images' directory must contain PNG files to be tested.
#   - The server must be running locally on port 5002 and have an endpoint '/predict' that accepts file uploads.
#
# Example:
#   Place your PNG files in the 'test_images' directory and run this script to get predictions.
for image_file in test_images/*.png; do
    echo "Testing $image_file"
    curl -X POST -F "file=@$image_file" http://localhost:5002/predict
    echo "\n"
done
