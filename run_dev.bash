#!/bin/bash
export POSTGRES_USER="postgres"
export POSTGRES_PASSWORD="3pP49KAMpd0HefyA"
export POSTGRES_DBNAME="prices_prod"
export POSTGRES_HOST="127.0.0.1"
python application/main.py $1