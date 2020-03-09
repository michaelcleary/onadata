#!/bin/bash

#sleep 20

#psql -h $FORMHUB_DB_SERVER -U postgres -c "CREATE ROLE onadata WITH SUPERUSER LOGIN PASSWORD '$PGPASSWORD';"
#psql -h $FORMHUB_DB_SERVER -U postgres -c "CREATE ROLE onadata LOGIN PASSWORD '$PGPASSWORD';"
#psql -h $FORMHUB_DB_SERVER -U postgres -c "CREATE DATABASE onadata OWNER onadata;"
psql -h $FORMHUB_DB_SERVER -U postgres onadata -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;"

#echo post psql, pre venv
virtualenv -p `which $SELECTED_PYTHON` /srv/onadata/.virtualenv/${SELECTED_PYTHON}
. /srv/onadata/.virtualenv/${SELECTED_PYTHON}/bin/activate

export DJANGO_SETTINGS_MODULE=onadata.settings.env_var_settings

cd /srv/onadata
#pip install --upgrade pip
#yes w | pip install -r requirements/base.pip

echo about to migrate
python manage.py migrate --noinput
echo about to collect
python manage.py collectstatic --noinput
echo about to runserver
python manage.py runserver 0.0.0.0:8000
