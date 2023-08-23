python3 manage.py makemigrations users
python3 manage.py makemigrations api
python3 manage.py makemigrations events
python3 manage.py migrate
# python manage.py loaddata dump.json
python3 manage.py collectstatic --no-input
python3 manage.py import_data --write_cities
python3 manage.py import_data --write_types
