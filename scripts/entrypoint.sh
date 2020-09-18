#!/bin/sh

set -e

python3 manage.py collectstatic --noinput
python3 manage.py migrate

uwsgi --socket :8000 --enable-threads --module cronProjectAPI.wsgi