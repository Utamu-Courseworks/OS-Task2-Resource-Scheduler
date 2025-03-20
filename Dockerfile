# Using an official Python runtime as a parent image
FROM python:3.9-slim

# Setting the working directory in the container
WORKDIR /app

# Copying the current directory contents into the container at /app
COPY . /app

# Installing any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Making port 5000 available to the world outside the container
EXPOSE 5000

# Defining environment variable
ENV NAME=World


# Running the app.py when the container launches
CMD ["python", "app.py"]
