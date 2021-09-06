# Setup your python development environment

### Pull sources from repository 
    git clone git@ssh.dev.azure.com:v3/CloudCompetenceCenter/Amsterdam-App/Amsterdam-App-Backend

### Branches
The _master_ branch is the current stable release where the _develop_ branch (made from _master_) is the upcoming
stable. From the _develop_ feature branches are derived and merged back on _develop_

e.g. timeline:

    O(0)    master -
    B(1)        - develop
                    - feature x  
                    - feature y
    M(2)        - develop + feature x
                    - feature y
    M(3)        - develop + feature x + feature y
    M(4)    master - new develop
                - develop
                
    O original, B branch, M merge, 0-n points in time
    
As you can see, it follows a reasonably normal git-flow.
                  
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

