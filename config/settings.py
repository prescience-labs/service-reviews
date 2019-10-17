import logging
import logging.config
import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
SENTRY_DSN  = os.getenv('SENTRY_DSN')
if SENTRY_DSN is not None and ENVIRONMENT is not 'development' and ENVIRONMENT is not 'test':
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=ENVIRONMENT,
    )
    print('Sentry logging initialized')

BASE_DIR                    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY                  = os.getenv('SECRET_KEY')
DEBUG                       = os.getenv('DEBUG', 'false').lower() == 'true'
ALLOWED_HOSTS               = os.getenv('ALLOWED_HOSTS', 'localhost,0.0.0.0').split(',')
CORS_ORIGIN_ALLOW_ALL       = os.getenv('CORS_ORIGIN_ALLOW_ALL', 'false').lower() == 'true'
CORS_ORIGIN_WHITELIST       = os.getenv('CORS_ORIGIN_WHITELIST').split(',') if os.getenv('CORS_ORIGIN_WHITELIST') else []
CORS_ORIGIN_REGEX_WHITELIST = os.getenv('CORS_ORIGIN_REGEX_WHITELIST') if os.getenv('CORS_ORIGIN_REGEX_WHITELIST') else []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',

    'common.apps.CommonConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF    = 'config.urls'
APPEND_SLASH    = False

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

# Admin site
# https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#adminsite-attributes
ADMIN_SITE = {
    'site_title': 'Reviews admin',
    'site_header': 'Reviews administration',
    'index_title': 'Reviews administration',
}

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)

# Auth
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
LANGUAGE_CODE   = 'en-us'
TIME_ZONE       = 'UTC'
USE_I18N        = True
USE_L10N        = True
USE_TZ          = True

# Static files
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Logging
# Logging
LOG_LEVEL       = os.getenv('LOG_LEVEL', 'DEBUG').upper()
LOGGING_CONFIG  = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(levelname)-8s %(asctime)s %(name)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        # root logger
        '': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
        },
        'django.utils.autoreload': {
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'INFO',
        },
    },
})

# Django Rest Framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    # 'EXCEPTION_HANDLER': 'common.services.exceptions.api_error_handler',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'list',
}

# Other services
DOCUMENTS_SERVICE = {
    'BASE_URL': os.getenv('DOCUMENTS_SERVICE_BASE_URL'),
}
MAILER_SERVICE = {
    'BASE_URL':             os.getenv('MAILER_SERVICE_BASE_URL'),
    'FROM_EMAIL':           os.getenv('MAILER_SERVICE_FROM_EMAIL', 'postmaster@mg.altamir.io'),
    'DEFAULT_DELAY_DAYS':   int(os.getenv('MAILER_SERVICE_DEFAULT_DELAY_DAYS', 0 if DEBUG else 7)),
}
AUTH_SERVICE = {
    'BASE_URL': os.getenv('AUTH_SERVICE_BASE_URL'),
}
