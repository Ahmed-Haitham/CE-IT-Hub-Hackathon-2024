# Dockerfile

# pull the official docker image
FROM node:20.11.1-alpine

# set work directory
WORKDIR /front

COPY neuro/package*.json ./

RUN npm config set strict-ssl false
# install dependencies
RUN npm install

# copy project - running from front context
COPY . ./

# set work directory
WORKDIR /front/neuro

CMD [ "npm", "start" ]