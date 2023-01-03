# Epic Events

Project 12



## Setup

clone the repo:
```sh
git clone https://github.com/BNNJ/Project9 {path/to/project}
```
move to the directory:
```sh
cd {path/to/project}
```

### virtual environment and dependancies

create a virtual environment:
```sh
python -m venv venv
```
enter the virtual environment (Linux/MacOS):
```sh
source venv/bin/activate
```
enter the virtual envirionment (Windows PowerShell):
```sh
.\venv\Scripts\Activate.ps1
```
install dependancies:
```sh
pip install -r requirements.txt
```

### database

At this point, you'll need to setup a postgreSQL database:  
[see their documentation](https://www.postgresql.org/docs/current/tutorial-install.html)

The application requires three environment variables:
- EE_DB_NAME: the database name
- EE_DB_USER: the username of a user with access to the database
- EE_DB_PASSWORD: the password of the user defined above

migrate base data to the database:
```sh
python manage.py migrate
```
This will add the necessary groups, statuses, etc. to the database.  

Note that if no migration is applied (if you previously applied the migrations then flush the database for example), you will need to reverse existing migrations first:
```sh
python manage.py migrate api zero
```
Then apply the migrations.

## usage

Some basic users are provided through the `python -m manage.py seed` command,  
but you can chose to make your own instead:

create a superuser:
```sh
python manage.py createsuperuser
```
and follow the instructions.
You can then add users for the sales and support groups.

run the webserver:
```sh
python manage.py runserver
```

Then open a web browser and enter the url `localhost:8000`  
or [click here](http:localhost:8000)  
