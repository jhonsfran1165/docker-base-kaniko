FROM node:14.18.1-alpine
RUN npm config set unsafe-perm true
RUN yarn global add npm@7.24.2
RUN apk update && apk add curl bash python3 g++ make automake autoconf libtool nasm libjpeg-turbo-dev ttf-opensans && rm -rf /var/cache/apk/*
RUN curl -sfL https://install.goreleaser.com/github.com/tj/node-prune.sh | bash -s -- -b /usr/local/bin

RUN wget -qO- "https://github.com/dustinblackman/phantomized/releases/download/2.1.1a/dockerized-phantomjs.tar.gz" | tar xz -C /

WORKDIR /app

RUN npm i imagemin-webp@6.0.0
RUN npm i imagemin-pngquant@9.0.2
RUN npm i imagemin-mozjpeg@7.0.0

RUN rm package-lock.json && rm package.json
