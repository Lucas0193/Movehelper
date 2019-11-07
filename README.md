# cs561-Project  

Movehelper webapp

Aim: people can find someone want to help them to move.

Develop environment: Python(3.7), Flask, SQLite, virtualenv.

Direction:

Before the direction, please install the Python(3.7), and Virtualenv.

$ cd myproject

$ python3 -m venv venv (in mac)

$ py -3 -m venv venv (in windows)

$ . venv/bin/activate (in mac)

/venv/Script/activate (in windows)

Notice: the folder "Movehelper" must name as "movehelper" (We'll fix this issue in next version.)

$ (venv) flask run

then you can begin to develop and test

if you want to run the unittests, enter" python -m unittest discover -v "

#! you may need to use pip tool to install some package.

$ pip install Flask

$ pip install python-dotenv

$ pip install Flask-Migrate

$ pip install Flask-SQLAlchemy

$ pip install flask-login

$ pip install flask-wtf

$ pip install flask-mail

$ pip install Flask-DotEnv

$ pip install bootstrap-flask

$ pip install Flask-CKEditor

We offer a package list "packages.txt" to help you install these packages.

please enter "pip install -r packages.txt"

#! If you want to initialize the DataBase.

please enter "flask initdb --drop"
