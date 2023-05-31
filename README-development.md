# Setup your python development environment

### Pull sources from repository 
    git clone git@ssh.dev.azure.com:v3/CloudCompetenceCenter/Amsterdam-App/Amsterdam-App-Backend

### Install development requirements
    pip install -r requirements-devtools.txt

### Create container on m1 arch for amd64
    
    docker buildx build --platform=linux/amd64 . -t registry-ams.luscinia-solutions.com/backend-api:tst-latest
    docker buildx build --platform=linux/amd64 . -t registry-ams.luscinia-solutions.com/backend-api:prd-latest

### Run pylinter

    pylint $(find . -name '*.py' | grep -v -e venv -e migrations -e kladblok)

### Branches
The _main_ branch is the current stable release where the _main_ branch (made from _main_) is the upcoming
stable. From the _develop_ feature branches are derived and merged back on _develop_

e.g. timeline:

    O(0)    main -
    B(1)        - develop
                    - feature x  
                    - feature y
    M(2)        - develop + feature x
                    - feature y
    M(3)        - develop + feature x + feature y
    M(4)    main - new develop
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
 
### Install the libraries needed for this project
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

By setting the 'DEBUG' environment parameter to true, it will set the following settings:

    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    DEBUG = True

**Do not set DEBUG=true in production!**

You can export the environment parameter like this:

    export DEBUG=true

## Enable searching in psql database

    ┌(robert@garthim.masikh.org)-(jobs:0)-(/Users/.3./Amsterdam-App-Backend)-(31 files,688b)
    └> 502 ● docker exec -it b37c1b96cbe2 bash
    root@b37c1b96cbe2:/# psql -h localhost -p 5432 -U backend -d amsterdam_app_backend -W
    Password: 
    psql (13.4 (Debian 13.4-1.pgdg100+1))
    Type "help" for help.
    
    amsterdam_app_backend=# CREATE EXTENSION pg_trgm;
    amsterdam_app_backend=# CREATE EXTENSION unaccent;

Once you have setup above extensions django needs an empty migration: 

    ./manage.py makemigrations --empty amsterdam_app_api
    ./manage.py migrate

