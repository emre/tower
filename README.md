# tower

A REST api implementation on the top of Hivemind

# Installation

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
