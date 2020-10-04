# project

To get started with the project, goto the directory containing project.

# if you don't have python in ur pc then consider installing python first
# after then upgrade the pip
>>> python3 -m pip install --user --upgrade pip
# verify ur installation 
>>> python3 -m pip --version
# install virtual environment
>>> python3 -m pip install --user virtualenv (linux)
>>> py -m pip install --user virtualenv (windows)

# create a virtual environment
>>> python3 -m venv projectenv(linux)

>>> py -m venv projectenv(windows)

# activate virtual environment
>>> source projectenv/Scripts/activate

# now cd inside your project and run following command
>>> pip install -r requirements.txt

# now run
>>> python manage.py migrate
>>> python manage.py runserver

# now you open your browser and goto http://127.0.0.1:8000
:)


## create a super user or admin 
>>> python manage.py createsuperuser
  and please fill the details as per your requirement

## Admin panel lies at url : http://127.0.0.1:8000/admin (input the login details as you'd created for superuser)


## About the technologies we use

we use python programming language (we have used python3). Python 3 is the version of python. Python is used as backend programming langauge. We have used Django framework for our project which is a popular web backend framework.

We have used html, css, javascript and jquery for frontend part.

We have used sqlite database to store data.

