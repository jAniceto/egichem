# egichem
Django based website for the EGICHEM group

## Running localy

Make sure you have Python and Pip and then install Pipenv:
```
$ pip install pipenv
```

Clone project repository and:
```
$ cd myproject
```

Install from Pipfile, if there is one:
```
$ pipenv install
```

Run development server:
```
$ pipenv run python manage.py runserver
```
Or by specifying the local settings file:
```
$ python manage.py runserver --settings=egichem.settings_local
```

Alternativelly you can set settings module:
```
$ set DJANGO_SETTINGS_MODULE=egichem.settings_local
```
then no longer needed to specify settings:
```
$ python manage.py runserver
```


# Deploy to Heroku

```
$ heroku login
$ git push heroku master
```

If deploying from a local branch other than master, e.g. testbranch:

```
$ git push heroku testbranch:master
```

Migrate database to the Heroku app:

```
$ heroku run python manage.py migrate
```

or 

```
$ heroku run python manage.py migrate <app_name>
```


# Deploy to VPS

```
cd egichem
source venv/bin/activate
cd egichem
python manage.py makemigrations [appname]
python manage.py migrate [appname]
python manage.py collectstatic
sudo systemctl restart gunicorn
```