FROM node:16 AS development
ENV NODE_ENV development

WORKDIR /usr/src/app

COPY package*.json /usr/src/app
COPY /public /usr/src/app/public

RUN npm install

EXPOSE 3000

CMD [ "npm", "start" ]