FROM node:16.14.0-alpine
RUN npm config set unsafe-perm true
RUN apk update && apk add curl bash python3 g++ make automake autoconf libtool nasm libjpeg-turbo-dev && rm -rf /var/cache/apk/*
RUN curl -sfL https://install.goreleaser.com/github.com/tj/node-prune.sh | bash -s -- -b /usr/local/bin

WORKDIR /app

RUN npm i imagemin-webp@6.0.0
RUN npm i imagemin-pngquant@9.0.2
RUN npm i imagemin-mozjpeg@7.0.0

RUN rm package-lock.json && rm package.json
