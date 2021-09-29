FROM node:14.16.0-alpine
RUN apk update && apk add curl bash python3 g++ make automake autoconf libtool nasm libjpeg-turbo-dev ttf-opensans && rm -rf /var/cache/apk/*
RUN curl -sfL https://install.goreleaser.com/github.com/tj/node-prune.sh | bash -s -- -b /usr/local/bin
RUN npm install -g npm@7.19.1
