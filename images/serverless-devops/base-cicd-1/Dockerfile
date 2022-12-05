# `python-base` sets up all our shared environment variables
FROM python:3.8-slim

# add the right variables
ARG SERVERLESS_VERSION=3.15.2

ARG COMMIT_ID
ARG PROJECT_VERSION
ENV PROJECT_VERSION="${PROJECT_VERSION}"

LABEL author="jhonsfran"                                 \
    org.opencontainers.image.revision="$COMMIT_ID"       \
    org.opencontainers.image.version="$PROJECT_VERSION"  \
    org.opencontainers.image.authors="KIS"

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    SERVERLESS_VERSION="${SERVERLESS_VERSION}" \
    # default app path
    APP_PATH="/opt/app" \
    # default user
    APP_USER="kis" \
    DEV_DEPS="tini bash" \
    BUILD_DEPS="build-essential curl git libpcre3 libpcre3-dev mime-support default-libmysqlclient-dev"

SHELL ["/bin/bash", "-o", "pipefail", "-o", "errexit", "-u", "-c"]

# INFO: install in one command. Not so good for debugging but improves size
# hadolint ignore=DL3018,DL3015,DL3008,SC2086
RUN set -ex; \
    # install dependencies
    apt-get update; \
    apt-get install -y --no-install-recommends $DEV_DEPS $BUILD_DEPS; \
    # install node
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -; \
    apt-get install -y nodejs; \
    # Create a group and user
    groupadd $APP_USER && useradd kis -g $APP_USER -u 1000 -m; \
    # Install v0.2 su-exec
    curl -o /usr/local/bin/su-exec.c \
    https://raw.githubusercontent.com/ncopa/su-exec/v0.2/su-exec.c; \
    gcc -Wall /usr/local/bin/su-exec.c -o/usr/local/bin/su-exec; \
    chown root:root /usr/local/bin/su-exec; \
    chmod 0755 /usr/local/bin/su-exec; \
    rm /usr/local/bin/su-exec.c; \
    # install docker cause serverless need docker to build images
    curl -fsSL https://get.docker.com -o get-docker.sh; \
    sh get-docker.sh; \
    rm get-docker.sh; \
    # create app dir and grant permissions
    mkdir -p "$APP_PATH"; \
    chown $APP_USER:$APP_USER -R "$APP_PATH"; \
    # clean apt
    apt-get clean; \
    npm config set prefix /usr/local; \
    npm install -g "serverless@${SERVERLESS_VERSION}"; \
    rm -rf /var/lib/apt/lists/*

# Copying in our entrypoint
COPY --chown=$APP_USER:$APP_USER ./bin/common-scripts /opt/scripts
RUN ["chmod", "-R", "+x", "/opt/scripts/"]

WORKDIR /opt/app

# this image can be used in development mode so we grant root permissions by default
# hadolint ignore=DL3002
USER root
# use tini to handle process PID 1
ENTRYPOINT ["/usr/bin/tini", "--", "/opt/scripts/entrypoint.sh"]
