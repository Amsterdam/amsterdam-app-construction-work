#!/usr/bin/env bash
sudo docker-compose -f docker-compose.yml --env-file ./env up --build --remove-orphans db
