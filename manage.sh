#! /usr/bin/env bash

source .env

export DB_HOST=localhost
export DB_PASS
export DB_USER
export DB_NAME
export APP_HOST
export DEBUG=True

python app/manage.py "$@"
