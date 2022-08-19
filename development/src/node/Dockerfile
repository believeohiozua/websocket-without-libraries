#  Dockerfile for Node Express Backend

FROM node:latest

# Create App Directory
RUN mkdir -p /usr/src/app
WORKDIR /code

# Install Dependencies
COPY ./src/package*.json ./

RUN yarn install --silent

# Copy app source code
COPY . .

# Exports
EXPOSE 5000

CMD ["yarn","run","start"]