# tower

A REST api implementation on the top of Hivemind

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

# Static files and Nginx

Add a STATIC_ROOT variable to your `local_settings.py` to serve the static files.

```
STATIC_ROOT = "/var/www/tower/static"
```

Note: Path should be created manually.

Run collectstatic command

```
$ python manage.py collectstatic
```

Serve the app and static files with nginx: (Example config)

```
server {
  server_name tower.emrebeyler.me;
  location / {
    include proxy_params;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    # we don't want nginx trying to do something clever with
    # redirects, we set the Host: header above already.
    proxy_redirect off;
    #proxy_set_header Host $host;
    proxy_pass http://0.0.0.0:8000;
  }
    location /static {
        autoindex on;
        alias /var/www/tower/static;
    }

}

```

# Docker installation

```
$ git clone https://github.com/emre/tower.git
$ vim docker/local_settings.py
$ docker build -t tower .
$docker run -d -p 8003:8000 tower
20fc6576d4e7992bd187299f614f39581f656db3550248b1d202666de3afa157
$ docker logs 20fc6576d4e7992bd187299f614f39581f656db3550248b1d202666de3afa157
[uWSGI] getting INI configuration from /app/docker/uwsgi.ini
[uwsgi-static] added check for /app/static-files
```

It's now, accessible at :8003.