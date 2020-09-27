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
>>> source projectenv/bin/activate

# now cd inside your project and run following command
>>> pip install -r requirements.txt

# now run
>>> python manage.py migrate
>>> python manage.py runserver

# now you open your browser and goto http://127.0.0.1:8000
:)

