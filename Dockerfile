FROM python:3
ENV PYTHONUNBUFFERED=1

# Install CRON to the python container
RUN apt-get update  \
 && apt-get -y install --no-install-recommends cron netcat npm \
 && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt /code/
RUN cd /code \
 && python3 -m venv venv \
 && . venv/bin/activate \
 && venv/bin/pip install --upgrade pip wheel setuptools \
 && venv/bin/pip install -r requirements.txt

# Setup run script
COPY init.sh /code/
RUN chmod +x /code/init.sh

# Copy sources to container
COPY env /code/
COPY static /code/static
COPY manage.py /code/
COPY create_user.py /code/
COPY README.md /code/
COPY README-development.md /code/
COPY vue_web_code /code/vue_web_code
COPY amsterdam_app_backend /code/amsterdam_app_backend
COPY amsterdam_app_api /code/amsterdam_app_api
