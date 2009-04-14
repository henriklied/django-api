# django-api
**Very early in development**

The aim of this project is to make it easier to create a manageable, public API for your site.
In it's current form it only makes displaying API documentation very easy, but the rest of the features are in development.

Features:
    - Automatic documentation for each API method (with sample usage in Python)
    - Application for API keys and management of these
    - API rate limiting
    - Usage monitoring



## Requirements
- Django 1.0 (or trunk)
- simplejson
- [uri](http://github.com/jacobian/uri/tree/master) by Jacob Kaplan-Moss

## Installation
Add the 'django_api' directory somewhere on your 'PYTHONPATH', put it into 'INSTALLED_APPS' in your settings file.
Fill in your information either in 'django_api/app_settings.py' or in your global settings file.

- Add this line to your Django project's urlconf: 
    url(r'^api/', include('django_api.urls')),

You're good to go!