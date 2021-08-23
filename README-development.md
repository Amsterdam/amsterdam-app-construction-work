# Setup your python development environment

### Pull sources from repository 
    git clone git@ssh.dev.azure.com:v3/CloudCompetenceCenter/Amsterdam-App/Amsterdam-App-Backend
 
### Setup virtual python environment
    cd Amsterdam-App-Backend
    python3 -m venv venv
 
### Activate your environment (needs to be done in every new shell!)
    source venv/bin/activate
 
### Update your pip, wheel and setuptools
    venv/bin/pip install --upgrade pip wheel setuptools
 
### Install the libraries needded for this project
    venv/bin/pip install -r requirements.txt

### Create Database environment
    chmod +x set_env.py && ./setenv.sh

### Start database in docker container
    chmod +x start_db.sh && sudo ./start_db.sh

### Clean your environment and start over
    chmod +x make_clean.sh && sudo ./make_clean.sh

### Remove your database credentials
    rm env

### Enable/Disable DEBUG mode

By setting the environment parameter to true, it will set the following settings:

    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    DEBUG = True

By setting the environment parameter to true, it will set the following settings:

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    DEBUG = False

**Do not set DEBUG=true in production!**

You can export the environment parameter like this:

    export DEBUG=true

