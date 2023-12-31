# Courier-income-calculation-backend
A System to calculate courier's daily and weekly income based on the travels ,bonuses and penalties.

## How to run

After cloning the repository you need to install python virtual environment

```bash 
  pip install virtualenv
```

Then you should create a python virtual environment. Run the following command at root directory

```bash 
  python -m venv .venv
```
After that activate the virtual environment

```bash 
  .\.venv\Scripts\activate 
```

Then we need to install dependencies

```bash 
  pip install -r .\requirements.txt
```
This version has migrations and tables so you just need to runserver

```bash 
  python manage.py runserver
```
This will run django server at localhost:8000. 
You can access admin page at localhost:8000/admin/ . The username is 'admin' and the password is '1234'.

