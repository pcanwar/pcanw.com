# pcanw.com

[pcanw.com](https://pcanw.com) 

# Blog

The website is inclouding:
  
  - webpage.
  - API: uses only a get method although commented other methods
  - Rss.

### Installation

Requires [python](https://python.org/) v3 to run.

You need to install a virtual environment work as I am using venv.

 a directory to work with:
```sh
$ cd pcanw.com
```
Create a new virtual environment inside the directory:
```sh
$ python3 -m venv env 
```

To use this environment’s packages, you need to “activate” it:
```sh
source env/bin/activate
(env) $ pip3 install -r requirements.txt
```
- makemigrations: to generates the SQL commands
- migrate: to update the database to the latest version of the Django models
- collectstatic: to collect the static files
- createsuperuser: to create and set up a superuser:


```sh
(env) $ python manage.py migrate
(env) $ python manage.py makemigrations
(env) $ python3 manage.py collectstatic
(env) $ python3 manage.py createsuperuser
```


Launch the development server:
```sh
$ python3 manage.py runserver
```

```sh
Starting development server at http://127.0.0.1:8000/
```


### Todos

 - push the settings file after removing the sensitive info for security purpose

License
----
GPL-2.0
