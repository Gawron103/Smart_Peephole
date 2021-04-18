#!/bin/bash

source ./SmartPeephole/env/bin/activate
gunicorn --threads 5 --workers 1 --bind xxx.xxx.x.xxx:xxxx app:app
