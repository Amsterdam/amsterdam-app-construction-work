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

FROM python:3.9-alpine as deploy
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on

# Install python requirements
COPY --from=build-phase1 /code/static /code/static
COPY requirements.txt /code/
COPY init.sh /code/
COPY manage.py /code/
COPY create_user.py /code/
COPY main_application /code/main_application
COPY construction_work /code/construction_work
COPY uwsgi.ini /code/uwsgi.ini
COPY nginx.conf /etc/nginx/nginx.conf

# Install dependencies
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && apk add --no-cache \
         bash \
         netcat-openbsd \
         procps \
         postgresql-client \
         libffi-dev libheif-dev libde265-dev \
         pcre pcre-dev  \
         nginx \
         mailcap \
    && cd /code \
    && python3 -m pip --no-cache-dir install -r /code/requirements.txt \
    && rm -rf /tmp/* \
    # && find / -name "*.c" -delete \
    # && find / -name "*.pyc" -delete \
    && apk del .build-deps \
    && chmod +x /code/init.sh
