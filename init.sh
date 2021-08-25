#!/bin/bash

###
#
# DOCKER ENTRY SCRIPT FOR STARTING UP THE AMSTERDAM BACKEND
#
# Touch /code/DEBUG, kill python process and run python manage.py [...] manually for debugging inside the docker
# container
#
###

function db_alive_check {
  state=0
  printf "checking for database"
  while ! nc -q 1 ${POSTGRES_HOST} 5432 </dev/null 1> /dev/null 2> /dev/null; do
    case $state in
      0) printf "\rchecking for database: -";;
      1) printf "\rchecking for database: \\";;
      2) printf "\rchecking for database: |";;
      3) printf "\rchecking for database: /";;
    esac
    [ "${state}" = "3" ] && state=0 || state=$((state+1))
    sleep 0.1
  done
  printf '\rchecking for database -> db alive\n'
}

function header {
    printf "\nInitializing Amsterdam-App-Backend\n"
}

function enable_python_venv {
   printf "\nEnabling python venv\n"
   cd /code && source venv/bin/activate
}

function make_migrations {
    printf "\nRunning DB migrations scripts ... "
    cd /code && python manage.py makemigrations amsterdam_app_api
    cd /code && python manage.py migrate
    printf "Done.\n"
}

function add_cron_jobs {
    printf "\nRemoving old cronjobs ... "
    cd /code && python manage.py crontab remove
    printf "Done.\n"
    printf "\nSetting new cronjobs ... "
    cd /code && python manage.py crontab add
    printf "Done.\n"
}

function add_static_files {
    printf "\nCollecting static add_static_files\n"
    cd /code && python manage.py collectstatic --no-input
}

function start_backend {
    printf "\nStarting Django API server\n\n"
    cd /code && python manage.py runserver 0.0.0.0:8000
}

function infinity_loop {
  while true; do
    # Touch /code/DEBUG, kill python process and run python manage.py [...] manually for debugging...
    if [[ ! -f "/code/DEBUG" ]]
    then
	    start_backend;
    fi
    sleep 1
  done
}

db_alive_check
header
enable_python_venv
make_migrations
add_cron_jobs
add_static_files
infinity_loop
