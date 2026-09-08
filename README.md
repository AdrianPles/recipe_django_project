This is my django web server, for recipe management.

Language: RO

Web pages:
http://127.0.0.1:8000/accounts/register/
http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/accounts/delete_confirm/
http://127.0.0.1:8000/  --> Home page
http://127.0.0.1:8000/create_recipe/
http://127.0.0.1:8000/delete_recipe/{pk}/
http://127.0.0.1:8000/update_recipe/{pk}/
http://127.0.0.1:8000/?category=all&by=title&sort=asc


To get started, run:
python -m venv .venv

make sure you activate the virtual environment after running the previous command. 

To activate it, run in Power Shell:
.\.venv\Scripts\activate

Then run:
pip install -r requirements.txt

This will setup your virtual env, and install the required packages.

To start the webserver, run:

python manage.py runserver



