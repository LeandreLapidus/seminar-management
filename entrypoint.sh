#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
./wait-for-it.sh db:7731 -- python manage.py runserver 0.0.0.0:7744
exec "$@"