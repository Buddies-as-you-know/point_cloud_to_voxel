# Use the official Open3D image as a base image
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any additional needed packages specified in requirements.txt
# Uncomment the line below if you have a requirements.txt file
# RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "app.py"]
