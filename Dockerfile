# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install poetry
RUN apt update && pip install poetry

# Set the working directory in the container
COPY . .

# Install dependencies
RUN poetry install

# Run the application asyncronously
CMD poetry run uvicorn --host 0.0.0.0 --lifespan off --port 5002 ssp:asgi_app