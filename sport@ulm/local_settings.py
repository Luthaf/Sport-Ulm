# -*- coding: utf-8 -*-
"""
Local settings for sport@ulm project.

"""

from django.conf import settings
import os

BASE_DIR = settings.BASE_DIR


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#(iid=)(g0o(fzy_ty2f^c-zsc*h@y2rgblq!b07(a^_!@4$i!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "media")
