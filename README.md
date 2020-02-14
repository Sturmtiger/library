# Web application "Library"
# About project
This app will consist of 3 pages:
1. List of books page
2. Book detail page
3. Book's author page

The book has a publisher company.

The book can be rated on a 10-point scale

3 types of users:
1. Administrator
2. User-Publisher
3. Reader

In addition to the usual registration,
there are opportunities to log in from social networks.

It is possible to send out new books to users once a week (on Fridays).



# How to run
1 variant: Open your terminal in this project and  just enter `docker-compose up`

2 variant(manually):
- pipenv install
- python3 manage.py migrate
- python3 manage.py loaddata library_data.json
- python3 manage.py runserver
