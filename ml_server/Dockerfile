# Use a base image compatible with ARM64
FROM --platform=linux/arm64 python:3.9-slim-buster

# Set environment variables to avoid buffering and set the working directory
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose the port
EXPOSE 5002

# Run the application
CMD ["python", "app.py"]
