# Use an official Python runtime as the parent image
FROM python:3.9.12-slim

WORKDIR /usr/src/app
COPY . /usr/src/app


# Install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available outside this container
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py using Flask's built-in server when the container launches
CMD ["flask", "run"]