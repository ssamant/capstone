# Capstone project


This site offers a tool small-scale farmers can use to collect and manage CSA subscriptions (Community Supported Agriculture is a model through which people can subscribe to a share of the produce grown on the farm, typically delivered in a weekly box). Through this application, users can sign up for a csa and farmers and see signups and member info. Online payments are not currently supported.

A working version of this app can be seen at: **[Lovelace Farm](https://www.lovelacefarm.com)**

This application was built using Django 1.11 and Python 3.6 with a PostgreSQL back-end database.

#### Setup and Installation:
1. You will need the following to run this app:
  * Python 3.6
  * A github account so you can clone this repo
  * Virtualenv
  * Django 1.11
  * git and pip for the command line

2.  Clone this repo into a project folder on your local machine. Set up a virtualenv.

3. pip install libraries from the requirements.txt file (I believe the one you need that won't come with Django is psycopg, which is needed to run the app with a PostgreSQL database).

4. Activate your virtual environment: source <virtual-env-name>/bin/activate
5. Set up you local database: python manage.py migrate

6. This app comes with seed data; if you want to use it:
python manage.py makemigrations members.json users.json locations.json signups.json seasons.json

7. Create a superuser, which will allow you to access the admin console
python manage.py createsuperuser

8. Users on the site are categorized into Farmer and Member groups. Create these groups through the admin console (under Authentication and Authorization). Users created through the app will automatically be assigned to the Member group. Assign a user to the Farmer group through the admin console (this is a non-ideal workaround that should be addressed in a future update).

9. Start you local server: python manage.py runserver

10. Point your browser to: http://127.0.0.1:8000/  
