#!/usr/bin/env bash
echo "Removing existing database"
rm db.sqlite3

echo "Removing existing migrations"
rm -r amsterdam_app_api/migrations
