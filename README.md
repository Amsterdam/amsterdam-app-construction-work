# Pre-requisites

Make sure your docker environment is up and running and you have a recent version of docker-compose installed.

# Build and start the Amsterdam-App-Backend

run: docker-compose up --build --remove-orphans

Example output:

    ┌(robert@darkcrystal)-(jobs:0)-(/home/<.3.>/amsterdam_app_backend)
    └> 660 ● docker-compose up --build --remove-orphans
    Building api-server
    Sending build context to Docker daemon  830.5kB
    Step 1/7 : FROM python:3
     ---> 59433749a9e3
    Step 2/7 : ENV PYTHONUNBUFFERED=1
     ---> Using cache
     ---> 43000305fa00
    Step 3/7 : WORKDIR /code
     ---> Using cache
     ---> cc58be29219a
    Step 4/7 : COPY requirements.txt /code/
     ---> Using cache
     ---> df4b2f93a48e
    Step 5/7 : RUN pip install -r requirements.txt
     ---> Using cache
     ---> 6692a2578400
    Step 6/7 : COPY . /code/
     ---> Using cache
     ---> b5b44ec255c1
    Step 7/7 : RUN chmod +x /code/init.sh
     ---> Using cache
     ---> dbd75b2aa343
    Successfully built dbd75b2aa343
    Successfully tagged amsterdam_app_backend_api-server:latest
    Starting amsterdam_app_backend_api-server_1 ... done
    Attaching to amsterdam_app_backend_api-server_1
    api-server_1  | 
    api-server_1  | Initializing Amsterdam-App-Backend
    api-server_1  | 
    api-server_1  | Running DB migrations scripts ... No changes detected
    api-server_1  | Operations to perform:
    api-server_1  |   Apply all migrations: admin, amsterdam_app_api, auth, contenttypes, sessions
    api-server_1  | Running migrations:
    api-server_1  |   No migrations to apply.
    api-server_1  | Done.
    api-server_1  | 
    api-server_1  | Starting Django API server
    api-server_1  | 
    api-server_1  | Watching for file changes with StatReloader
    api-server_1  | Performing system checks...
    api-server_1  | 
    api-server_1  | System check identified no issues (0 silenced).
    api-server_1  | August 09, 2021 - 11:08:54
    api-server_1  | Django version 3.2.6, using settings 'amsterdam_app_backend.settings'
    api-server_1  | Starting development server at http://0.0.0.0:8000/
    api-server_1  | Quit the server with CONTROL-C.

# Database 

The Amsterdam-App-Backend will make use of the postgress database server. This hasn't been implemented
yet. The current data storage in use is a tinysql database.

# Get initial data

Make sure your application is running on port 8000 on your localhost. Now open the url below in your
browser of choice to fetch initial data or update existing data. This end-point will disappear in the
near future in favour of a cron-job. 

    http://localhost:8000/api/projects/ingest

# Current implemented APIs (v1)

    Fetch initial data:
         
        /api/projects/v1/ingest
        Valid query (mandatory) parameter: project-type=['brug', 'kade']
        
        e.g: http://localhost:8000/api/v1/projects/ingest?project-type=kade

    Get all projects:
     
        /api/v1/projects
        Valid query (optional) parameter: project-type=['brug', 'kade']

        e.g: http://localhost:8000/api/v1/projects/ingest?project-type=kade

    Get project details:

        /api/v1/project/details
        Valid query (mandatory) parameter: id=sting (md5 hash, identifier from /api/projects)

        e.g. http://localhost:8000/api/v1/project/details?id=846f78938721bd84db735dd413c63346

(other APIs are pending...)
