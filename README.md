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



# How to run (locally)
Open your terminal in this project and  just enter `docker-compose up`

# How to run (deploy on Heroku)
1. Sign up on Heroku
2. Install Heroku `sudo snap install --classic heroku`
3. Login in `heroku login`
4. Create new app `heroku create`
5. Add secret key from **settings.py** to Heroku env var 
`heroku config:set SECRET_KEY=YOUR_DJANGO_SECRET_KEY -a your-app-name`
6. Add the Heroku app URL to the list of ALLOWED_HOSTS in **settings.py**
like this `ALLOWED_HOSTS = ['localhost', '127.0.0.1', '<your-app-name.herokuapp.com>']`
7. `heroku container:login`
8. Build docker image `sudo docker build -t registry.heroku.com/<your-app-name>/web -f deploy/Dockerfile .`
9. Push the image to the registry `sudo docker push registry.heroku.com/<your-app-name>/web`
10. Release the image `heroku container:release -a <your-app-name> web`
11. Try running `heroku open -a <your-app-name>` to open the app in your default browser.