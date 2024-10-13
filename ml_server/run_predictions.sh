for image_file in test_images/*.png; do
    echo "Testing $image_file"
    curl -X POST -F "file=@$image_file" http://localhost:5002/predict
    echo "\n"
done
