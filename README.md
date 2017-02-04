Django-IsMigrated
=================

Django-IsMigrated is a simple Django app that tells you if a Django project 
has been migrated or not.  It exits with Zero if there are not migrations, and 
NonZero if there are. 

For Django 1.7, 1.8 and 1.9 use v0.x.x

Quick start
-----------

1. Add "django-ismigrated" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-ismigrated',
    ]

2. Run `python manage.py ismigrated` to determine if there are migrations to run.

Authors
-------
* Austin Lally: alally@concentricsky.com
* Francisco Gray: fgray@concentricsky.com
