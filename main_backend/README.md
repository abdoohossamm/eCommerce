# main_backend

This is an eCommerce REST API backend project built with django and django rest framework.

The API root url is: /api/v1/

#### Applications included:
* store: The core app for the project that include the product, category, review, and album models with their ViewSets and serializers.
    * Products API
    * Categories API
    * Reviews API
    * Album API

* users: The users app that store the users data and has the auth user model (CustomUser model).
  * users API

* orders: The orders app the stores the orders data in Order Model.
  * orders API

## Run the project

Make sure you are in main_backend directory

Make a virtual environment:
```bash
python -m venv venv
```
Activate the virtual environment:
* linux:
```bash
source venv/bin/activate
```

* windows:
```bash
venv\Scripts\activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

Make a copy of the example environment variables file and call it `.env`:
```bash
cp .env.example .env
```
Edit the environmental variables and enter your variables 

NOTE: if left without edit the application will run but PayPal payment won't work

Run migrations:
```bash
python manage.py migrate
```

Create superuser:
```bash
python manage.py createsuperuser
```

Run server:
```bash
python manage.py runserver
```

now you have the server running go to 
http://127.0.0.1:8000/api/v1/
and see the API

you can go to http://127.0.0.1:8000/admin
to sign in as a superuser then go to the api url.
