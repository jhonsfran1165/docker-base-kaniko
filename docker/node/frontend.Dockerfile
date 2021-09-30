FROM node:14.16.0-alpine
RUN apk update && apk add curl bash python3 g++ make automake autoconf libtool nasm libjpeg-turbo-dev ttf-opensans && rm -rf /var/cache/apk/*
RUN curl -sfL https://install.goreleaser.com/github.com/tj/node-prune.sh | bash -s -- -b /usr/local/bin

RUN wget -qO- "https://github.com/dustinblackman/phantomized/releases/download/2.1.1a/dockerized-phantomjs.tar.gz" | tar xz -C /
