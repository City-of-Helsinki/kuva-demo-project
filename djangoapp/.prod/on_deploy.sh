#!/bin/bash

python /app/manage.py migrate --noinput

# Generate the admin user
# If no password is set, the admin user gets a generated password which will
# be written in stdout so that it can be accessed during the initial deployment.
if [[ "$ADMIN_USER_PASSWORD" ]]; then
    DJANGO_SUPERUSER_PASSWORD=$ADMIN_USER_PASSWORD DJANGO_SUPERUSER_USERNAME=kuva-admin DJANGO_SUPERUSER_EMAIL=kuva-admin@hel.ninja python /app/manage.py createsuperuser --noinput
else
    DJANGO_SUPERUSER_USERNAME=kuva-admin DJANGO_SUPERUSER_EMAIL=kuva-admin@hel.ninja python /app/manage.py createsuperuser --noinput
fi
