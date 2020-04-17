FROM python:3.7

RUN apt-get update
RUN apt-get -y install supervisor
RUN pip3 install pipenv

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /library_project

WORKDIR /library_project

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system

COPY . .

RUN python manage.py collectstatic --noinput


COPY deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD supervisord -c /etc/supervisor/supervisord.conf && gunicorn Library.wsgi:application --bind 0.0.0.0:$PORT
#CMD celery -A Library.celery_app worker -B -l INFO -Q send_mail,newsletter && gunicorn Library.wsgi:application --bind 0.0.0.0:$PORT
