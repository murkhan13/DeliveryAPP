#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --socker :8000 --master --enable-threads --module cronDeliveryAPI.wsgi
