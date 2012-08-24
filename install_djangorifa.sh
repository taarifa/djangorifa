#!/bin/bash
DATABASE_NAME=djangorifa
DATABASE_USER=djangorifa

# Set the PostGIS version
if [ -z "$1" ]; then
  PGIS_VERSION=1.5
else
  PGIS_VERSION="$1"
fi

# Create the spatial database
POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib/postgis-$PGIS_VERSION
exists=`psql --list | egrep '\btemplate_postgis\b'`

# Check if the template_postgis database exists. If not, create it.
if [ -z "$exists" ]; then
  # Creating the template spatial database.
  createdb -E UTF8 template_postgis
  createlang -d template_postgis plpgsql # Adding PLPGSQL language support.
  # Allows non-superusers the ability to create from this template
  psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
  # Loading the PostGIS SQL routines
  psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql
  psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
  # Enabling users to alter spatial tables.
  psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
  psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
  psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
fi

# Create a new djangorifa user - will prompt for a password but nothing else
createuser -P -D -R -S $DATABASE_USER
createdb -T template_postgis -E 'utf8' -O $DATABASE_USER $DATABASE_NAME

# Install the requirements
../bin/pip install psycopg2
../bin/pip install django-celery
../bin/pip install django-admin-tools
../bin/pip install South
../bin/pip install django-mailer
../bin/pip install django-registration
../bin/pip install django_extensions
../bin/pip install django_nose
../bin/pip install django_mobile
../bin/pip install django-crispy-forms
../bin/pip install django-generic-m2m
../bin/pip install django-sendsms

# Syncdb all and migrate fake
../bin/python djangorifa/manage.py syncdb --all
../bin/python djangorifa/manage.py migrate --fake
