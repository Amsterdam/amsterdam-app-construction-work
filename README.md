[![Build Status](https://dev.azure.com/CloudCompetenceCenter/Amsterdam-App/_apis/build/status/Amsterdam-App-Backend?branchName=main)](https://dev.azure.com/CloudCompetenceCenter/Amsterdam-App/_build/latest?definitionId=480&branchName=main)
[![Build Status](https://dev.azure.com/CloudCompetenceCenter/Amsterdam-App/_apis/build/status/Amsterdam-App-Backend?branchName=develop)](https://dev.azure.com/CloudCompetenceCenter/Amsterdam-App/_build/latest?definitionId=480&branchName=develop)

# Pre-requisites

Make sure your docker environment is up and running and you have a recent version of docker-compose installed.

### API documentation

If the backend is running, you can visit the online api documentation

```
    http://localhost:8000/api/v1/apidocs
```

The definition for the api documentation are in the file 'views_swagger_auto_schema.py'

### Developer documentation:
README-development.md Here you can find among other settings e.g. how to enable debug mode.

### Setup your database credentials
```
    run: chmod +x set_env.py && ./set_env.py
```

**Example output:**

```
    Please enter your POSTGRES database (default: amsterdam_app_backend): 
    Please enter your POSTGRES username (default: backend): 
    Please enter your POSTGRES password (or use: 94ADsLnM): 
    Save values to environment? (Y/N/A(bort)): N
    Please enter your POSTGRES database (default: amsterdam_app_backend): 
    Please enter your POSTGRES username (default: backend): 
    Please enter your POSTGRES password (or use: flr5fbjH): MyS3cr3t                
    Save values to environment? (Y/N/A(bort)): y
```

**Your environment will look like:**

```
    POSTGRES_PASSWORD=MyS3cr3t
    POSTGRES_USER=backend
    POSTGRES_DB=amsterdam_app_backend
```

## Build and start the Amsterdam-App-Backend

```
    sudo docker-compose -f docker-compose.yml --env-file ./env up --build --remove-orphans
```

**Note**:

The docker must run **sudo** because the database files are unreadable for normal users. This will prevent the build step
from succeeding and hence the docker containers won't start.

**Example output**:

```
    sudo docker-compose -f docker-compose.yml --env-file ./env up --build --remove-orphans
    Docker Compose is now in the Docker CLI, try `docker compose up`
    
    Building api-server
    [+] Building 1.1s (15/15) FINISHED                                                                                       
     => [internal] load build definition from Dockerfile                                                                0.0s
     => => transferring dockerfile: 541B                                                                                0.0s
     => [internal] load .dockerignore                                                                                   0.0s
     => => transferring context: 2B                                                                                     0.0s
     => [internal] load metadata for docker.io/library/python:3                                                         0.7s
     => [internal] load build context                                                                                   0.0s
     => => transferring context: 40.85kB                                                                                0.0s
     => [ 1/10] FROM docker.io/library/python:3@sha256:28ba68f41f73354b3cfca4af3e4d55cf553761ae25797c41b303f8fa219e7ad  0.0s
     => => resolve docker.io/library/python:3@sha256:28ba68f41f73354b3cfca4af3e4d55cf553761ae25797c41b303f8fa219e7ade   0.0s
     => CACHED [ 2/10] RUN apt-get update   && apt-get -y install --no-install-recommends cron netcat  && rm -rf /var/  0.0s
     => CACHED [ 3/10] WORKDIR /code                                                                                    0.0s
     => CACHED [ 4/10] COPY requirements.txt /code/                                                                     0.0s
     => CACHED [ 5/10] RUN pip install -r requirements.txt                                                              0.0s
     => [ 6/10] COPY init.sh /code/                                                                                     0.0s
     => [ 7/10] RUN chmod +x /code/init.sh                                                                              0.2s
     => [ 8/10] COPY manage.py /code/                                                                                   0.0s
     => [ 9/10] COPY amsterdam_app_backend /code                                                                        0.0s
     => [10/10] COPY amsterdam_app_api /code                                                                            0.0s
     => exporting to image                                                                                              0.0s
     => => exporting layers                                                                                             0.0s
     => => writing image sha256:bcbb3008b21155c7600f2ced3d345494f43532131ffcd351925eb13a9fea2dda                        0.0s
     => => naming to docker.io/library/amsterdam-app-backend_api-server                                                 0.0s
    
    Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
    Successfully built bcbb3008b21155c7600f2ced3d345494f43532131ffcd351925eb13a9fea2dda
    Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
    Recreating amsterdam-app-backend_db_1 ... done
    Recreating amsterdam-app-backend_api-server_1 ... done
    Attaching to amsterdam-app-backend_db_1, amsterdam-app-backend_api-server_1
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
    db_1          | syncing data to disk ... initdb: warning: enabling "trust" authentication for local connections
    db_1          | You can change this by editing pg_hba.conf or using the option -A, or
    db_1          | --auth-local and --auth-host, the next time you run initdb.
    db_1          | ok
    db_1          | 
    db_1          | 
    db_1          | Success. You can now start the database server using:
    db_1          | 
    db_1          |     pg_ctl -D /var/lib/postgresql/data -l logfile start
    db_1          | 
    db_1          | waiting for server to start....2021-08-17 09:02:19.479 UTC [48] LOG:  starting PostgreSQL 13.4 (Debian 13.4-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
    db_1          | 2021-08-17 09:02:19.480 UTC [48] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
    db_1          | 2021-08-17 09:02:19.491 UTC [49] LOG:  database system was shut down at 2021-08-17 09:02:18 UTC
    db_1          | 2021-08-17 09:02:19.504 UTC [48] LOG:  database system is ready to accept connections
    db_1          |  done
    db_1          | server started
    db_1          | CREATE DATABASE
    db_1          | 
    db_1          | 
    db_1          | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
    db_1          | 
    db_1          | 2021-08-17 09:02:20.890 UTC [48] LOG:  received fast shutdown request
    db_1          | waiting for server to shut down...2021-08-17 09:02:20.891 UTC [48] LOG:  aborting any active transactions
    db_1          | .2021-08-17 09:02:20.892 UTC [48] LOG:  background worker "logical replication launcher" (PID 55) exited with exit code 1
    db_1          | 2021-08-17 09:02:20.893 UTC [50] LOG:  shutting down
    db_1          | 2021-08-17 09:02:20.918 UTC [48] LOG:  database system is shut down
    db_1          |  done
    db_1          | server stopped
    db_1          | 
    db_1          | PostgreSQL init process complete; ready for start up.
    db_1          | 
    db_1          | 2021-08-17 09:02:21.024 UTC [1] LOG:  starting PostgreSQL 13.4 (Debian 13.4-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
    db_1          | 2021-08-17 09:02:21.024 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
    db_1          | 2021-08-17 09:02:21.024 UTC [1] LOG:  listening on IPv6 address "::", port 5432
    db_1          | 2021-08-17 09:02:21.027 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
    db_1          | 2021-08-17 09:02:21.048 UTC [76] LOG:  database system was shut down at 2021-08-17 09:02:20 UTC
    db_1          | 2021-08-17 09:02:21.066 UTC [1] LOG:  database system is ready to accept connections
    checking for database -> db alivebase
    api-server_1  | 
    api-server_1  | Initializing Amsterdam-App-Backend
    api-server_1  | 
    api-server_1  | Running DB migrations scripts ... Migrations for 'amsterdam_app_api':
    api-server_1  |   amsterdam_app_api/migrations/0001_initial.py
    api-server_1  |     - Create model Image
    api-server_1  |     - Create model ProjectDetails
    api-server_1  |     - Create model Projects
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
    api-server_1  | Removing old cronjobs ... no crontab for root
    api-server_1  | Done.
    api-server_1  | 
    api-server_1  | Setting new cronjobs ...   adding cronjob: (96b481d2adb3bab4fa3be5a2ddc51875) -> ('0 */4 * * *', 'amsterdam_app_backend.cron.run')
    api-server_1  | Done.
    api-server_1  | 
    api-server_1  | Starting Django API server
    api-server_1  | 
    api-server_1  | Watching for file changes with StatReloader
    api-server_1  | Performing system checks...
    api-server_1  | 
    api-server_1  | System check identified no issues (0 silenced).
    api-server_1  | August 17, 2021 - 09:02:25
    api-server_1  | Django version 3.2.6, using settings 'amsterdam_app_backend.settings'
    api-server_1  | Starting development server at http://0.0.0.0:8000/
    api-server_1  | Quit the server with CONTROL-C.
    api-server_1  | [17/Aug/2021 09:14:37] "GET /api/v1/projects/ingest?project-type=kade HTTP/1.1" 200 83
    api-server_1  | Not Found: /favicon.ico
    api-server_1  | [17/Aug/2021 09:14:37] "GET /favicon.ico HTTP/1.1" 404 2230
    api-server_1  | [17/Aug/2021 09:14:54] "GET /api/v1/projects/ingest?project-type=brug HTTP/1.1" 200 83
    api-server_1  | [17/Aug/2021 09:14:58] "GET /api/v1/projects HTTP/1.1" 200 116225
    api-server_1  | [17/Aug/2021 09:15:26] "GET /api/v1/image?id=472ead77645cf72865013a314cb96aa4 HTTP/1.1" 200 62186
```

### Database 

The Amsterdam-App-Backend will make use of the postgres database server. Use setenv.sh script for setting your 
credentials. Database files will be stored in '/data/db' folder in your project root.

### Get initial data

Make sure your application is running on port 8000 on your localhost. Now open the url below in your
browser of choice to fetch initial data or update existing data. This end-point will disappear in the
near future in favour of a cron-job. 

```
    http://localhost:8000/api/v1/projects/ingest
    Valid (mandatory) query parameter: project-type=['brug', 'kade']
```

### API documentation

There is online API documentation available at:
```
    http://localhost:8000/api/v1/apidocs
```

There is offline documentation available at:
```
    /amsterdam_app_api/swagger_views_*.py
```

### Garbage collector

When a content item was seen before but not in the last Iprox scrape, the content item will be marked inactive. 
If the content item has been marked inactive for over 1 week, the content item and its siblings will be removed.

    Siblings are: Warning-messages, News items, Project, Project details, subscriptions for phones, authorizations for project-managers and so forth.
