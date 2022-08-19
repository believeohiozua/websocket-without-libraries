#  Dockerfile for Node Express Backend

# FROM python:3.8-slim-buster
FROM python:latest


# Create Work Directory
WORKDIR /src

# Copy app source code
COPY . .

# Install Dependencies
RUN pip install -r requirements.txt


# Exports
EXPOSE 5000

CMD [ "python3", "server.py", "run", "--host=0.0.0.0", "--port=5000" ]