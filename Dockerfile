FROM node:latest
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
RUN rm package*.json

COPY public ./public
COPY YepYouDeservedIt ./YepYouDeservedIt
COPY index.js ./index.js

RUN apt-get update && apt-get install -y locales && locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

RUN chown -R node /usr/src/app/public/CSSSR_Page/TASKS_UPLOADER

USER node 
CMD [ "node", "index.js" ]