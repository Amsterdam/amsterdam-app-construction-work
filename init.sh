#!/bin/bash

###
#
# DOCKER ENTRY SCRIPT FOR STARTING UP THE AMSTERDAM APP BACKEND
#
# touch /code/DEBUG, kill python process and run python manage.py [...] manually for debugging inside the docker
# container
#
###

function is_db_alive {
  state=0
  printf "checking for database"
  while ! nc -q 1 ${POSTGRES_HOST} ${POSTGRES_PORT} </dev/null 1> /dev/null 2> /dev/null; do
    case $state in
      0) printf "\rchecking for database: -";;
      1) printf "\rchecking for database: \\";;
      2) printf "\rchecking for database: |";;
      3) printf "\rchecking for database: /";;
    esac
    [ "${state}" = "3" ] && state=0 || state=$((state+1))
    sleep 0.1
  done
  printf '\rChecking for database -> db alive\n'
}

function enable_db_text_search {
  printf "\nEnable text search in database\n"
  PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -h ${POSTGRES_HOST} -c "CREATE EXTENSION IF NOT EXISTS pg_trgm CASCADE;"
  PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -h ${POSTGRES_HOST} -c "CREATE EXTENSION IF NOT EXISTS unaccent CASCADE;"
  # PGPASSWORD=${POSTGRES_PASSWORD} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -h ${POSTGRES_HOST} -c "CREATE EXTENSION IF NOT EXISTS earthdistance CASCADE;"
}

function set_header {
    printf "\nInitializing Amsterdam-App-Backend\n"
}

function make_migrations {
    printf "\nRunning DB migrations scripts ... "
    cd /code && python manage.py makemigrations amsterdam_app_api
    cd /code && python manage.py migrate
    printf "Done.\n"
}

function add_static_files {
    printf "\nCollecting static add_static_files\n"
    cd /code && python manage.py collectstatic --no-input
}

function create_user {
    printf "\nCreating web-users\n"
    cd /code && python create_user.py
}

function start_backend {
    printf "\nStarting Django API server (uwsgi)\n\n"
    cd /code && uwsgi --ini uwsgi.ini
}

function start_nginx {
    printf "\nStarting Nginx server\n\n"
    cd /code && nginx -g "daemon off;" &
}

function enter_infinity_loop {
  if [ -z ${UNITTEST} ]; then
    while true; do
      # Touch /code/DEBUG, kill uwsgi processes and run python manage.py [...] manually for debugging...
      if [[ ! -f "/code/DEBUG" ]]
      then
        start_backend;
      fi
      sleep 1
    done
  else
    printf "Starting unittests\n\n"
    cd /code && python manage.py test
  fi      
}

is_db_alive
enable_db_text_search
set_header
make_migrations
create_user
add_static_files
start_nginx
enter_infinity_loop
