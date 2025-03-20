# Use an official Python image
FROM python:3.9-slim

# Install system dependencies for Tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Command to run the application
CMD ["python", "app.py"]
