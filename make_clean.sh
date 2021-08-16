#!/usr/bin/env bash
echo "Removing existing database (requires sudo)"
sudo rm -rf data

echo "Removing existing migrations"
sudo rm -r amsterdam_app_api/migrations
