#!/bin/bash

function header {
    printf "\nInitializing Amsterdam-App-Backend\n"
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

header
make_migrations
add_cron_jobs
infinity_loop
