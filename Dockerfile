FROM python:alpine3.6
RUN apk update
RUN apk add --no-cache gcc python3-dev libc-dev libressl-dev postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk add --no-cache musl-dev linux-headers

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install uwsgi
RUN mkdir -p /app/static-files/static
COPY . /app
RUN mv /app/docker/local_settings.py /app/docker/tower
RUN python manage.py collectstatic --no-input
ENTRYPOINT ["uwsgi", "--ini", "/app/docker/uwsgi.ini"]
