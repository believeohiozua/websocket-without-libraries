# FROM python:3.8-slim-buster
FROM python:latest

# Create Work Directory
WORKDIR /src

# Copy app source code
COPY . .

# Install Dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN  docker run --publish 5000:5000 ws python3 server.py 0.0.0.0:5000

# Exports
EXPOSE 80

CMD [ "python3", "server.py", "run", "--host=0.0.0.0", "--port=8000"]