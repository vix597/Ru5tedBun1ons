"""
Django settings for rustedbunions project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from .utils import get_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPLOY_PUBLIC_DIR = os.path.join("/", "home", "public", "rustedbunions")
DEPLOY_PROTECTED_DIR = os.path.join("/", "home", "protected")
SECRET_KEY_FILE = os.path.join(BASE_DIR, "django_secret_key")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#
# This is not the key used in production, however if you're seeing this flag
# in the source code on github...it is valid...it's the only flag in the source
# code that I didn't change. Great Job! You're looking in the right places.
#
SECRET_KEY = 'flag{ack*acc3$s}'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["www.rustedbunions.com"]

if DEBUG:
    ALLOWED_HOSTS = []
if not DEBUG:
    SECRET_KEY = get_secret_key(SECRET_KEY_FILE)  # Creates the key if it doesn't exist

# Application definition

INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'crapdb.apps.CrapdbConfig',
    'leaderboard.apps.LeaderboardConfig',
    'traveler.apps.TravelerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rustedbunions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rustedbunions.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

if DEBUG:
    DATABASE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
    CRAPDB_PATH = os.path.join(BASE_DIR, 'crapdb.sqlite3')
else:
    DATABASE_PATH = os.path.join(DEPLOY_PROTECTED_DIR, "database", "db.sqlite3")
    CRAPDB_PATH = os.path.join(DEPLOY_PROTECTED_DIR, "database", 'crapdb.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(DEPLOY_PUBLIC_DIR, "static")
