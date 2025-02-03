"""
Project name = website
dajngo version = 3.1.6.
python version = 3.8.10

"""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'l+bg8q)%&l6md7=s-bqmen$_e224u$8@ll8=-8tth-vd6ndt_i'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [

    #Website apps
    'core',
    'users.apps.UsersConfig',
    'story',
    'notifications',

    #Default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Third party apps
    'django_cleanup.apps.CleanupConfig', 
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

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'website/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.views.CountNotifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


#Databases setting

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files setting (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

#Media file setting (user uploaded data)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


#Django by default's tuning
from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
message_constants.ERROR: 'danger',

}

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Ensures Django uses SMTP
EMAIL_USE_TLS = True  # Enables encryption via TLS (Transport Layer Security)
EMAIL_USE_SSL = False  # Must be False if TLS is True
EMAIL_HOST = 'smtp.gmail.com'  # Example for Gmail SMTP server
EMAIL_PORT = 587  # Correct port for TLS (Use 465 for SSL)
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your email address
EMAIL_HOST_PASSWORD = 'your-email-password'  # App password (not your email password)
DEFAULT_FROM_EMAIL = 'GeniusPen <your-email@gmail.com>'  # Sets sender name

#Login url
LOGIN_URL = 'users:login'

