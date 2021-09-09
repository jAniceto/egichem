# egichem
Django based website for the EGICHEM group

### Running localy

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