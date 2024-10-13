# Base image
FROM tensorflow/tfx:latest

# Set the working directory
WORKDIR /app

# Copy the pipeline code and data generation script
COPY pipeline/ ./pipeline/
COPY data/ ./data/

# Install any additional dependencies
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir tensorflow

# Run the data_gen.py script to generate data
RUN python data/data_gen.py

# Set environment variables if needed
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Run the pipeline
CMD ["python", "pipeline/pipeline.py"]
