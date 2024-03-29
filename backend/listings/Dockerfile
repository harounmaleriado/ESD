# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY . /usr/src/app

COPY main/firebase-adminsdk.json /app/firebase-adminsdk.json


ENV FIREBASE_ADMIN_KEY /app/firebase-adminsdk.json
ENV FLASK_APP=main/run.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["flask", "run"]
