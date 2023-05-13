# FairPay

This project is built with Python 3.8 and Django 4.2.

## Prerequisites

Before you start, make sure you have the following software installed:

- Python 3.8 or higher with pip.

## Installation

- Create a virtual environment using `python -m venv .venv` for windows and `virtualenv .venv` for Linux (optional).
- Install all dependencies using `pip install -r requirements.txt` or `pip3 install requirements.txt`.

## Execution

- Run django application using `python manage.py runserver 0.0.0.0:8000`.

## Notes

Postman collection available in `./docs` folder contains all endpoints used in the application, however if you want to test apis in production they are accessible via https://retropixel-8f415.uc.r.appspot.com.

PostreSQL is used in production environment however for local deployment application is configured for working with sqlite