# Use an official Python runtime as a parent image
FROM python:3.9.12-slim

WORKDIR /usr/src/app
COPY . /usr/src/app


# Install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["flask", "run"]
