FROM python:3
ENV PYTHONUNBUFFERED=1

# Install CRON to the python container
RUN apt-get update  \
 && apt-get -y install cron \
 && rm -rf /var/lib/apt/lists/*

# Set Workdir
WORKDIR /code

# Install python requirements
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Setup run script
COPY init.sh /code/
RUN chmod +x /code/init.sh

# Copy sources to container
COPY manage.py /code/
COPY amsterdam_app_backend /code
COPY amsterdam_app_api /code
