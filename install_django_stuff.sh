# Install the requirements
pip install -r requirements.txt

python djangorifa/manage.py syncdb --all
python djangorifa/manage.py migrate --fake
