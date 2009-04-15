# django-api
**Pretty early in development – but it works very well**

The aim of this project is to make it easier to create a manageable, public API for your site.
Be aware that this project in no way seeks to help you create an underlying API – that's up to you.

This project tries to be language agnostic. django_api doesn't care what language your API is originally written in. It only acts as a gateway between the user and the underlying API.

Current features:
    - Transparent API proxy for external developers / users
    - Automatic documentation for each API method (with automatic sample usage in Python)
    - API rate limiting
    - Usage monitoring (currently through the admin, not good enough)

Planned features:
    - Users should be able to apply for API keys, as they can using other services (e.g. Mashery)
    - Dedicated API admin panel
    - Transparent caching layers for intensive and much-used methods



## Requirements
- Django 1.0 (or trunk)
- simplejson

## Installation
- Add the 'django_api' directory somewhere on your 'PYTHONPATH'
- Put 'django_api' into 'INSTALLED_APPS' in your projects' settings file.
- Open django_api/app_settings.py and either fill out your settings there, or add them to your global settings file.

- Add this line to your Django project's urlconf: 
    url(r'^api/', include('django_api.urls')),

Then go to the admin interface and add your URLs! :)