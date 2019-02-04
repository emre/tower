# tower

A REST api implementation on the top of Hivemind

# Installation (Via docker)

1. Using the docker image

```
$ docker run -p 8090:8000 -e DB_PASS='hive' \
	-e DB_USER='hivemind_db_user' \
	-e DB_NAME='hivemind_db_name' \
	-e DB_PORT='5432' \
	-e DB_HOST='<hivemind_database_api>' \
	emrebeyler/tower:stable
```

2. Building by repository

Clone the repository:

```
$ git clone https://github.com/emre/tower.git
```

Build the Docker container:

```
$ docker build -t tower .
```

Run the container

```
$ docker run -p 8090:8000 -e DB_PASS='hive' \
	-e DB_USER='hivemind_db_user' \
	-e DB_NAME='hivemind_db_name' \
	-e DB_PORT='5432' \
	-e DB_HOST='<hivemind_database_api>' \
	tower
```

For troubleshooting, you may enable the debug mode with `DEBUG=1`. To 
check logs:

```
$ docker logs <container_id>
[uWSGI] getting INI configuration from /app/docker/uwsgi.ini
[uwsgi-static] added check for /app/static-files
```


# Installation (Manual)

```
$ git clone https://github.com/emre/tower.git
$ python3.6 -m venv tower-env
$ source tower-env/bin/activate
$ cd tower
$ pip install -r requirements.txt
```

# Configuration

```
$ vim tower/local_settings.py
```

Add database information of your Hivemind:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'host',
        'PORT': 'port',
    }
}

```

# Running

For development:

```
$ python manage.py runserver
```

For production:

```
$ gunicorn tower.wsgi
```
