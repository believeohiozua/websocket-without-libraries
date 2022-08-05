#  Dockerfile for Node Express Backend

FROM python:3.8-slim-buster

# Create App Directory
RUN mkdir -p /usr/src/app
WORKDIR /python

# Copy app source code
COPY . .

# Install Dependencies
RUN pip install -r requirements.txt


# Exports
EXPOSE 8000


CMD [ "python3", "server.py", "run", "--host=0.0.0.0"]