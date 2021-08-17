# Pre-requisites

Make sure your docker environment is up and running and you have a recent version of docker-compose installed.

### Developer documentation:
README-development.md

## Setup your database credentials

    run: chmod +x set_env.py && ./set_env.py

Example output:

    Please enter your POSTGRES database (default: amsterdam_app_backend): 
    Please enter your POSTGRES username (default: backend): 
    Please enter your POSTGRES password (use: 94ADsLnM): 
    Save values to environment? (Y/N/A(bort)): N
    Please enter your POSTGRES database (default: amsterdam_app_backend): 
    Please enter your POSTGRES username (default: backend): 
    Please enter your POSTGRES password (use: flr5fbjH): MyS3cr3t                
    Save values to environment? (Y/N/A(bort)): y

Your environment will look like:

    POSTGRES_PASSWORD=MyS3cr3t
    POSTGRES_USER=backend
    POSTGRES_DB=amsterdam_app_backend


## Build and start the Amsterdam-App-Backend

    sudo docker-compose -f docker-compose.yml --env-file ./env up --build --remove-orphans

Note:

The docker must run sudo because the database files are unreadable for normal users. This will prevent the build step
from succeeding and hence the docker containers won't start.

Example output:

    sudo docker-compose -f docker-compose.yml --env-file ./env up --build --remove-orphans
    Building api-server
    Sending build context to Docker daemon  65.02MB
    Step 1/10 : FROM python:3
     ---> 59433749a9e3
    Step 2/10 : ENV PYTHONUNBUFFERED=1
     ---> Using cache
     ---> 43000305fa00
    Step 3/10 : WORKDIR /code
     ---> Using cache
     ---> cc58be29219a
    Step 4/10 : COPY requirements.txt /code/
     ---> Using cache
     ---> 891636588616
    Step 5/10 : RUN pip install -r requirements.txt
     ---> Using cache
     ---> 0f403cf993e8
    Step 6/10 : COPY manage.py /code/
     ---> Using cache
     ---> d7074e3180e6
    Step 7/10 : COPY init.sh /code/
     ---> Using cache
     ---> dc9069abdd54
    Step 8/10 : RUN chmod +x /code/init.sh
     ---> Using cache
     ---> df198c58db81
    Step 9/10 : COPY amsterdam_app_backend /code
     ---> 360982467d79
    Step 10/10 : COPY amsterdam_app_api /code
     ---> 637bf34b68cb
    Successfully built 637bf34b68cb
    Successfully tagged amsterdam-app-backend_api-server:latest
    Starting amsterdam-app-backend_db_1 ... done
    Recreating amsterdam-app-backend_api-server_1 ... done
    Attaching to amsterdam-app-backend_db_1, amsterdam-app-backend_api-server_1
    api-server_1  | 
    api-server_1  | Initializing Amsterdam-App-Backend
    api-server_1  | 
    db_1          | The files belonging to this database system will be owned by user "postgres".
    db_1          | This user must also own the server process.
    db_1          | 
    db_1          | The database cluster will be initialized with locale "en_US.utf8".
    db_1          | The default database encoding has accordingly been set to "UTF8".
    db_1          | The default text search configuration will be set to "english".
    db_1          | 
    db_1          | Data page checksums are disabled.
    db_1          | 
    db_1          | fixing permissions on existing directory /var/lib/postgresql/data ... ok
    db_1          | creating subdirectories ... ok
    db_1          | selecting dynamic shared memory implementation ... posix
    db_1          | selecting default max_connections ... 100
    db_1          | selecting default shared_buffers ... 128MB
    db_1          | selecting default time zone ... Etc/UTC
    db_1          | creating configuration files ... ok
    db_1          | running bootstrap script ... ok
    db_1          | performing post-bootstrap initialization ... ok
    db_1          | syncing data to disk ... ok
    db_1          | 
    db_1          | 
    db_1          | Success. You can now start the database server using:
    db_1          | 
    db_1          |     pg_ctl -D /var/lib/postgresql/data -l logfile start
    db_1          | 
    db_1          | initdb: warning: enabling "trust" authentication for local connections
    db_1          | You can change this by editing pg_hba.conf or using the option -A, or
    db_1          | --auth-local and --auth-host, the next time you run initdb.
    db_1          | waiting for server to start....2021-08-16 14:08:04.073 UTC [49] LOG:  starting PostgreSQL 13.4 (Debian 13.4-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
    db_1          | 2021-08-16 14:08:04.076 UTC [49] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
    db_1          | 2021-08-16 14:08:04.084 UTC [50] LOG:  database system was shut down at 2021-08-16 14:08:03 UTC
    db_1          | 2021-08-16 14:08:04.090 UTC [49] LOG:  database system is ready to accept connections
    api-server_1  | Running DB migrations scripts ... /usr/local/lib/python3.9/site-packages/django/core/management/commands/makemigrations.py:105: RuntimeWarning: Got an error checking a consistent migration history performed for database connection 'default': could not connect to server: Connection refused
    api-server_1  | 	Is the server running on host "db" (172.19.0.2) and accepting
    api-server_1  | 	TCP/IP connections on port 5432?
    api-server_1  | 
    api-server_1  |   warnings.warn(
    db_1          |  done
    db_1          | server started
    api-server_1  | No changes detected in app 'amsterdam_app_api'
    db_1          | CREATE DATABASE
    db_1          | 
    db_1          | 
    db_1          | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
    db_1          | 
    db_1          | 2021-08-16 14:08:04.388 UTC [49] LOG:  received fast shutdown request
    db_1          | waiting for server to shut down....2021-08-16 14:08:04.391 UTC [49] LOG:  aborting any active transactions
    db_1          | 2021-08-16 14:08:04.393 UTC [49] LOG:  background worker "logical replication launcher" (PID 56) exited with exit code 1
    db_1          | 2021-08-16 14:08:04.394 UTC [51] LOG:  shutting down
    db_1          | 2021-08-16 14:08:04.412 UTC [49] LOG:  database system is shut down
    db_1          |  done
    db_1          | server stopped
    db_1          | 
    db_1          | PostgreSQL init process complete; ready for start up.
    db_1          | 
    db_1          | 2021-08-16 14:08:04.513 UTC [1] LOG:  starting PostgreSQL 13.4 (Debian 13.4-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
    db_1          | 2021-08-16 14:08:04.514 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
    db_1          | 2021-08-16 14:08:04.516 UTC [1] LOG:  listening on IPv6 address "::", port 5432
    db_1          | 2021-08-16 14:08:04.525 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
    db_1          | 2021-08-16 14:08:04.531 UTC [77] LOG:  database system was shut down at 2021-08-16 14:08:04 UTC
    db_1          | 2021-08-16 14:08:04.537 UTC [1] LOG:  database system is ready to accept connections
    api-server_1  | Operations to perform:
    api-server_1  |   Apply all migrations: admin, amsterdam_app_api, auth, contenttypes, sessions
    api-server_1  | Running migrations:
    api-server_1  |   Applying contenttypes.0001_initial... OK
    api-server_1  |   Applying auth.0001_initial... OK
    api-server_1  |   Applying admin.0001_initial... OK
    api-server_1  |   Applying admin.0002_logentry_remove_auto_add... OK
    api-server_1  |   Applying admin.0003_logentry_add_action_flag_choices... OK
    api-server_1  |   Applying amsterdam_app_api.0001_initial... OK
    api-server_1  |   Applying contenttypes.0002_remove_content_type_name... OK
    api-server_1  |   Applying auth.0002_alter_permission_name_max_length... OK
    api-server_1  |   Applying auth.0003_alter_user_email_max_length... OK
    api-server_1  |   Applying auth.0004_alter_user_username_opts... OK
    api-server_1  |   Applying auth.0005_alter_user_last_login_null... OK
    api-server_1  |   Applying auth.0006_require_contenttypes_0002... OK
    api-server_1  |   Applying auth.0007_alter_validators_add_error_messages... OK
    api-server_1  |   Applying auth.0008_alter_user_username_max_length... OK
    api-server_1  |   Applying auth.0009_alter_user_last_name_max_length... OK
    api-server_1  |   Applying auth.0010_alter_group_name_max_length... OK
    api-server_1  |   Applying auth.0011_update_proxy_permissions... OK
    api-server_1  |   Applying auth.0012_alter_user_first_name_max_length... OK
    api-server_1  |   Applying sessions.0001_initial... OK
    api-server_1  | Done.
    api-server_1  | 
    api-server_1  | Starting Django API server
    api-server_1  | 
    api-server_1  | Watching for file changes with StatReloader
    api-server_1  | Performing system checks...
    api-server_1  | 
    api-server_1  | System check identified no issues (0 silenced).
    api-server_1  | August 16, 2021 - 14:08:06
    api-server_1  | Django version 3.2.6, using settings 'amsterdam_app_backend.settings'
    api-server_1  | Starting development server at http://0.0.0.0:8000/
    api-server_1  | Quit the server with CONTROL-C.
    api-server_1  | Not Found: /favicon.ico
    api-server_1  | [16/Aug/2021 14:08:22] "GET /favicon.ico HTTP/1.1" 404 2232
    api-server_1  | Not Found: /favicon.ico
    api-server_1  | [16/Aug/2021 14:08:28] "GET /favicon.ico HTTP/1.1" 404 2230
    api-server_1  | [16/Aug/2021 14:08:44] "GET /api/v1/projects?project-type=kade HTTP/1.1" 200 30
    api-server_1  | [16/Aug/2021 14:09:06] "GET /api/v1/projects/ingest?project-type=kade HTTP/1.1" 200 83
    api-server_1  | [16/Aug/2021 14:09:23] "GET /api/v1/projects/ingest?project-type=brug HTTP/1.1" 200 83
    api-server_1  | [16/Aug/2021 14:09:43] "GET /api/v1/projects?project-type=brug HTTP/1.1" 200 34121
    api-server_1  | [16/Aug/2021 14:10:04] "GET /api/v1/image?id=ab9717c5c0d63107883f5a10039a0a3c HTTP/1.1" 200 42120

## Database 

The Amsterdam-App-Backend will make use of the postgres database server. Use setenv.sh script for setting your 
credentials. Database files will be stored in '/data/db' folder in your project root.

## Get initial data

Make sure your application is running on port 8000 on your localhost. Now open the url below in your
browser of choice to fetch initial data or update existing data. This end-point will disappear in the
near future in favour of a cron-job. 

    http://localhost:8000/api/projects/ingest

## Current implemented APIs (v1)

    Fetch initial data:
         
        /api/projects/v1/ingest
        Valid (mandatory) query parameter: project-type=['brug', 'kade']
        
        e.g: http://localhost:8000/api/v1/projects/ingest?project-type=kade

    Get all projects:
     
        /api/v1/projects
        Valid (optional) query parameter: project-type=['brug', 'kade']

        e.g: http://localhost:8000/api/v1/projects?project-type=kade

    Get project details:

        /api/v1/project/details
        Valid (mandatory) query parameter: id=sting (md5 hash, identifier from /api/projects)

        e.g. http://localhost:8000/api/v1/project/details?id=846f78938721bd84db735dd413c63346

    Get image:
    
        /api/vi/image
        Valid (mandatory) query parameter: id=string (md5 hash, indentifier from /api/project/details image object)
        
        e.g. http://localhost:8000/api/v1/image?id=0accad7dd900a72a7b2e3f16d6b50ad1

### Newer documentation?
During development of this project, this README.md file will be updated. Please return to this file if you pull new sources.