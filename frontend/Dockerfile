FROM node:9.11.1-alpine
RUN npm install -g yarn
RUN npm install -g http-server
RUN chmod +x /usr/local/bin/yarn
WORKDIR frontend/
COPY ./package.json /frontend/package.json
COPY . /frontend/
RUN yarn install
RUN yarn build
EXPOSE 8080
CMD ["http-server", "dist"]

