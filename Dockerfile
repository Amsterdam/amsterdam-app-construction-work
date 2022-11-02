FROM ubuntu:20.04 as build-phase1

# Set TZ-data environment
ENV TZ=Europa/Amsterdam

# Install base utils
RUN apt-get update \
 && DEBIAN_FRONTEND="noninteractive" TZ=$TZ apt-get -y install --no-install-recommends npm

# Add source
COPY vue_web_code /code/vue_web_code

# Build vue webside
RUN cd /code/vue_web_code \
 && npm install \
 && npm run build \
 && cp -r dist /code/static/

FROM python:3.9.0-slim-buster as deploy
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on

# Install python requirements
COPY requirements.txt /code/
RUN cd /code && python3 -m pip install -r requirements.txt

RUN apt-get update  \
 && apt-get -y install --no-install-recommends \
    netcat \
    procps \
    postgresql-client-11 \
 && rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old \
 && apt-get autoremove -y \
 && rm -rf /tmp/*

# Copy sources to container
COPY --from=build-phase1 /code/static /code/static
COPY init.sh /code/
COPY manage.py /code/
COPY create_user.py /code/
COPY amsterdam_app_backend /code/amsterdam_app_backend
COPY amsterdam_app_api /code/amsterdam_app_api

# Setup run script
RUN chmod +x /code/init.sh
