"""
Django settings for amsterdam_app_backend project.
"""
import os
from uuid import uuid4
from base64 import b64encode
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Create random security string on startup
SECRET_KEY = b64encode(str(uuid4()).encode('utf-8')).decode()

# Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as “secure”,
# which means browsers may ensure that the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = os.getenv('DEBUG', 'false').lower() != 'true'

# If this is set to True, the cookie will be marked as “secure”, which means browsers may ensure that the cookie is only
# sent under an HTTPS connection.
SESSION_COOKIE_SECURE = os.getenv('DEBUG', 'false').lower() != 'true'

# Whether to expire the session when the user closes their browser.
SESSION_EXPIRE_AT_BROWSER_CLOSE = os.getenv('DEBUG', 'false').lower() != 'true'

# Enable/Disable DEBUG mode
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
if not DEBUG:
    print('Django runs in PRODUCTION mode')
    print('You can enable DEBUG mode by setting the environment parameter DEBUG=true')
else:
    print('Django runs in DEBUG mode')
    print('You can disable DEBUG mode by removing the environment parameter DEBUG=true')

ALLOWED_HOSTS = ['*']

# NGINX reverse-proxy: X_FORWARDED_FOR will tell swagger the point of origin and adjusts its links accordingly
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django_nose',
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'amsterdam_app_api.apps.AmsterdamAppApiConfig'
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
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = ['deviceid']
ROOT_URLCONF = 'amsterdam_app_backend.urls'

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


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    #'DEFAULT_AUTHENTICATION_CLASSES': [
    #    'rest_framework.authentication.TokenAuthentication'
    #]
}

#
WSGI_APPLICATION = 'amsterdam_app_backend.wsgi.application'

# Settings used for the api documentation services
SWAGGER_SETTINGS = {
    "SUPPORTED_SUBMIT_METHOD": ['get', 'post', 'put', 'delete'],
    'USE_SESSION_AUTH': False,
    "LOGIN_URL": "/",
    "LOGOUT_URL": "/",
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'description': 'Personal API Key authorization',
            'name': 'Authorization',
            'in': 'header',
        }
    },
    'APIS_SORTER': 'alpha',
    "SHOW_REQUEST_HEADERS": True,
    "VALIDATOR_URL": None,
    'api_key': '',
}

# CronJobs
CRONJOBS = [
    ('0 */4 * * *', 'amsterdam_app_backend.cron.run')
]

# Database credentials from environment variables
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '0.0.0.0')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))

# Setup database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT
    }
}

# The lifetime of a database connection, as an integer of seconds. Use 0 to close database connections at the end of
# each request — Django’s historical behavior — and None for unlimited persistent connections.
CONN_MAX_AGE = 0

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIR = []
STATIC_ROOT = "{base_dir}/static".format(base_dir=BASE_DIR)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--cover-package=amsterdam_app_api'
]
