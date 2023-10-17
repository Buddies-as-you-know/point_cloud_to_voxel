# Use an official Python runtime as a base image
FROM python:3.10-slim
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy just the requirements file and install dependencies
# This layer is rebuilt when requirements.txt changes
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# This layer is rebuilt when the application code changes
COPY . /app

# Run app.py when the container launches
CMD ["python", "src/main.py"]
