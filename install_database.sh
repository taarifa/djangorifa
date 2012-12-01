#!/bin/bash
DATABASE_NAME=djangorifa
DATABASE_USER=djangorifa

# Set the PostGIS version
if [ -z "$1" ]; then
  PGIS_VERSION=1.5
else
  PGIS_VERSION="$1"
fi

if ![ -f "djangorifa/django_config/local_settings.py" ]; then
  cat << EOF > "djangorifa/django_config/local_settings.py"
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'djangorifa',
        'USER': 'djangorifa',
        'PASSWORD': 'facebook',
        'HOST': 'localhost',
        'PORT': '',
    }
}
EOF
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

