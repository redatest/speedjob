# Django settings for speedjob project.
import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db549366168',         # Or path to database file if using sqlite3.
        'USER': 'dbo549366168',                      # Not used with sqlite3.
        'PASSWORD': 'guigui22',                  # Not used with sqlite3.
        'HOST': 'db549366168.db.1and1.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}


ALLOWED_HOSTS = ['www.speedjob.fr']


TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT    = '/kunden/homepages/11/d445074125/htdocs/media'

MEDIA_URL = '/media/'

# STATIC_ROOT = '/kunden/homepages/11/d445074125/htdocs/speedjob/static'
STATIC_ROOT = os.path.join( PROJECT_ROOT,  'static' )

# ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.i
    
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'dajaxice.finders.DajaxiceFinder',
)


SECRET_KEY = '2#3h@cf6osxw2r7)vd^e487ur@_5l%#39b&amp;^z8brsu9t44s4w%'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'speedjob.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'speedjob.wsgi.application'

TEMPLATE_DIRS = (

    os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates')),
)

FIXTURE_DIRS = (os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', "fixtures")), )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'suit',
    'django.contrib.admin',

    'app',

    'django_extensions',
    'crispy_forms',

    'payments',
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

CACHE_TIMEOUT = 60*60
# python manage.py createcachetable cached_results
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cached_results',
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
    
}



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

# email configuration

LOGIN_REDIRECT_URL = '/'

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "redatest7dev@gmail.com"
EMAIL_HOST_PASSWORD = 'redatest7'
EMAIL_PORT = 587

ACCOUNT_ACTIVATION_DAYS = 14


# Stripe payments

STRIPE_SECRET_KEY    = "sk_test_mopWUvH81IrewEKfXKN9e6rq"
STRIPE_PUBLIC_KEY    = "pk_test_v9t1PMYuYgsUM5Zsoj3uFn2b"

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
