#!/bin/sh

source ./server/env/bin/activate
gunicorn --threads 5 --workers 1 --bind 192.168.0.178:7070 app:app
