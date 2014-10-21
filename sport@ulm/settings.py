# -*- coding: utf-8 -*-
"""
Django settings for sport@ulm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'minimal'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

AUTH_USER_MODEL = 'profilENS.User'

INSTALLED_APPS += (
    'commons',
    'bds',
    'profilENS'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'sport@ulm.urls'
APPEND_SLASH = False

WSGI_APPLICATION = 'sport@ulm.wsgi.application'


TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),
                )


LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Europe/Paris'

USE_TZ = True

try:
    from .local_settings import *
except ImportError:
    pass
