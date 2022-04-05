FROM python:3.9.0-slim-buster
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on

# Install python requirements
COPY requirements.txt /code/
RUN apt-get update  \
 && apt-get -y install --no-install-recommends \
    netcat \
    vim \
    procps \
    postgresql-client-11 \
    curl \
    npm \
    nodejs \
 # Install Node and NPM \
 && rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old \
 && apt-get autoremove -y \
 && cd /code \
 && python3 -m pip install -r requirements.txt \
 && rm -rf /tmp/* \
 && npm -i g npm@latest \
 && npm cache clean -f \
 && npm install -g n \
 && n stable

# RUN npm install -g npm

# Install vue web code
COPY vue_web_code /code/vue_web_code

RUN cd /code/vue_web_code \
 && npm install --force \
 && npm run build \
 && rm -rf /code/vue_web_code/node_modules

# Copy sources to container
COPY init.sh /code/
COPY env /code/
COPY static /code/static
COPY manage.py /code/
COPY create_user.py /code/
COPY README.md /code/
COPY README-development.md /code/
COPY fcm_credentials.json /code/
COPY amsterdam_app_backend /code/amsterdam_app_backend
COPY amsterdam_app_api /code/amsterdam_app_api

# Setup run script
RUN chmod +x /code/init.sh
