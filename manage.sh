#! /usr/bin/env bash

source .env

export DB_HOST=localhost
export DB_PASS
export DB_USER
export DB_NAME
export API_HOST
export API_SECRET_KEY
export DEBUG=True

cd app && python manage.py "$@"
