# -*- coding: utf-8 -*-
import os
import sys
# PROJECT_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEBUG = True

# DATABASES = {'default': dj_database_url.config(default='postgres://localhost')} # heroku database settings

SECRET_KEY = 'qd@j3*it@3j2cgc#7t@m)^r1bnc53uam7o7u_+x$f5w3$b@5ix'
CRISPY_TEMPLATE_PACK = 'bootstrap'

TIME_ZONE = 'Europe/Paris'
USE_TZ = True

TEMPLATE_DEBUG = DEBUG
ADMINS = []
MANAGERS = ADMINS
LANGUAGE_CODE = 'fr-FR'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT    = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media'))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

MEDIA_URL          = '/media/'
STATIC_URL         = '/static/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'speedjob.urls'

TEMPLATE_DIRS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates'))

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'static')),
)

FIXTURE_DIRS = (os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "fixtures")), )

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'suit',
    'django.contrib.admin',

    'django.contrib.messages',

    'gunicorn',
    'django_extensions',
    'crispy_forms',

    'payments',
    'django_forms_bootstrap',
    'main',

    'pure_pagination',
    'car_shop',
    'dajaxice',
    'dajax',
    'registration',
    'profile',
    'article',
    'offre',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'fqa.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            # 'class': 'ssweb.logger.FQAdminEmailHandler',
            'class': 'logging.StreamHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console', 'default'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'SpeedJob administration',
    'SHOW_REQUIRED_ASTERISK': True,
    'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
    },
    'MENU_OPEN_FIRST_CHILD': True, 
    # 'MENU_EXCLUDE': ('auth.group','sites',),
    # 'MENU': (
    #     'sites',
    #     '-',
    #     'auth',
    #     '-',
    #     {'app': 'auth',     'label':'Utilisateurs avances', 'icon':'icon-lock',     'models': ('user', 'group')},
    #     '-',
    #     {'app': 'profile',  'label':'Profiles',             'icon':'icon-user',     'models': ('profile_emp','profile_candid', 'application') },
    #     '-',
    #     {'app': 'offre',    'label':'Offres',               'icon':'icon-envelope', 'models': ('offer',) },
    #     '-',
    #     {'app': 'article',  'label':'Article',              'icon':'icon-book',     'models': ('article',) },
    #     '-',
    # ),
}

CACHE_TIMEOUT = 60*60
# python manage.py createcachetable cached_results
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cached_results',
    }
}

PAYMENTS_INVOICE_FROM_EMAIL = 'redatest7@gmail.com'

PAYMENTS_PLANS = {
    "potato_normal": {
        "stripe_plan_id": "potato_normal",
        "name": "Monthly Potato Delivery",
        "description": "Monthly potato delivery to your door.",
        "price": 15,
        "currency": "gbp",
        "interval": "month"
    },

    "potato_premier": {
        "stripe_plan_id": "potato_premier",
        "name": "Monthly Premier Potato Delivery",
        "description": "Monthly PREMIER potato delivery to your door.",
        "price": 30,
        "currency": "gbp",
        "interval": "month",
    },
}

LOGIN_REDIRECT_URL = '/'

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "redatest7dev@gmail.com"
EMAIL_HOST_PASSWORD = 'redatest7'
EMAIL_PORT = 587

ACCOUNT_ACTIVATION_DAYS = 14

try:
    from local_settings import *
except ImportError:
    pass
