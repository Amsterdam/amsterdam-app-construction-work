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
