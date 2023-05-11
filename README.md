# FairPay Backend

This project was created using python3.8 and Django

## Run

- Create a virtual environment using `python -m venv .venv` for windows (optional)
- Install all dependencies using `pip install -r requirements.txt` or `pip3 install requirements.txt`
- Run django application using `python manage.py runserver 0.0.0.0:8000`

Postman collection available in `./docs` folder contains all endpoints used in the application, however if you want to test apis in production they are accessible via https://retropixel-8f415.uc.r.appspot.com.

PostreSQL is used in production environment however for local deployment application is configured for working with sqlite