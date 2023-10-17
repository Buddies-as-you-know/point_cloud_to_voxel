# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment, activate it, upgrade pip, and install dependencies
RUN python -m venv ./venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Run app.py when the container launches
CMD ["python", "src/main.py"]
