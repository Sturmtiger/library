FROM python:3.7

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

CMD gunicorn Library.wsgi:application --bind 0.0.0.0:$PORT