"""
Django settings for learninghub project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'znuytm9xhr_1u2pp70b2g@d4p5&(dda4&4gltxv(8lq649_z)y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
#TEMPLATE_DIRS = ("")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed learninghub projects
    'learningbucket',
    'searchbucket',
    'profilebucket',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'learninghub.urls'

WSGI_APPLICATION = 'learninghub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        # mySQL
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME':'learninghub',
#        'USER':'learninghub',
#        'PASSWORD':'1234',

        # Sqlite3 - uncomment this and add comments to mySQL 
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'nb_NO' 
#LANGUAGE_CODE = 'nb' 

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True

LANGUAGES = (('nb-no','Norwegian'),('en-us', 'English'))

#LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale/'))
LOCALE_PATHS = (os.path.abspath(os.path.join(BASE_DIR, 'locale')))
#LOCALE_PATH = "locale/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '../static/'

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = '../media/'

# LEARNING HUB settings
# Spesific settings for learninghub

SITE_URL = "http://127.0.0.1:8000"

# email 
EMAIL = "learninghub@test.com"

USER_SELF_REGESTRING = True
EMAIL_DOMAINS = [r'.*@gmail.com', r'.*@test.com']

# Shall the project be open for all
OPEN_PROJECTS = True
