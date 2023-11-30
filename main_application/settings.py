"""
Django settings for main_application project.
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Get random secret key from environment variable
SECRET_KEY = os.getenv("SECRET_KEY")

# When developing DJANGO_DEVELOPMENT is used to remove security
DJANGO_DEVELOPMENT = os.getenv("DJANGO_DEVELOPMENT", "false").lower() == "true"
if not DJANGO_DEVELOPMENT:
    print("Django runs in PRODUCTION mode")
else:
    print("Django runs in DEVELOPMENT mode")

# Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as “secure”,
# which means browsers may ensure that the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = True
if DJANGO_DEVELOPMENT:
    CSRF_COOKIE_SECURE = False

# If this is set to True, the cookie will be marked as “secure”, which means browsers may ensure that the cookie is only
# sent under an HTTPS connection.
SESSION_COOKIE_SECURE = True
if DJANGO_DEVELOPMENT:
    SESSION_COOKIE_SECURE = False

# Whether to expire the session when the user closes their browser.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
if DJANGO_DEVELOPMENT:
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# In Django, ALLOWED_HOSTS is a list of strings representing
# the host/domain names that the Django application can serve.
# This is a security measure to prevent HTTP Host header attacks.
allowed_hosts_all = ["*"]
allowed_hosts_limited = [
    "construction-work",  # Host within docker realm
    "api-backend.app-amsterdam.nl",
    "api-test-backend.app-amsterdam.nl",
    "api-dev-backend.app-amsterdam.nl",
]
ALLOWED_HOSTS = allowed_hosts_limited
if DJANGO_DEVELOPMENT:
    ALLOWED_HOSTS = allowed_hosts_all

# Enable/Disable DEBUG mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
if DEBUG:
    print("This app is running in DEBUG mode")

# NGINX reverse-proxy: X_FORWARDED_FOR will tell swagger the point of origin and adjusts its links accordingly
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Uncomment to enable Django Debug Toolbar
# Makes the API really slow returning data, don't know why
INTERNAL_IPS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "django_nose",
    "django_crontab",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "rest_framework",
    "rest_framework.authtoken",
    "construction_work.apps.ConstructionWorkApiConfig",
    "debug_toolbar",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    "deviceid",
    "deviceauthorization",
    "ingestauthorization",
    "userauthorization",
    "authorization",
    "x_forwarded_proto",
]
ROOT_URLCONF = "main_application.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    #'DEFAULT_AUTHENTICATION_CLASSES': [
    #    'rest_framework.authentication.TokenAuthentication'
    # ]
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

#
WSGI_APPLICATION = "main_application.wsgi.application"

# Settings used for the api documentation services
SWAGGER_SETTINGS = {
    "SUPPORTED_SUBMIT_METHOD": ["get", "post", "put", "delete"],
    "USE_SESSION_AUTH": False,
    "LOGIN_URL": "/",
    "LOGOUT_URL": "/",
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "description": "Personal API Key authorization",
            "name": "Authorization",
            "in": "header",
        }
    },
    "APIS_SORTER": "alpha",
    "SHOW_REQUEST_HEADERS": True,
    "VALIDATOR_URL": None,
    "api_key": "",
    "DEFAULT_MODEL_RENDERING": "example",
}

# CronJobs
CRONJOBS = [("0 */4 * * *", "main_application.cron.run")]

# Database credentials from environment variables
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER", "POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB", "POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

# Setup database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}

# To enable persistent connections, set CONN_MAX_AGE to a positive integer of seconds.
# For unlimited persistent connections, set it to None.
CONN_MAX_AGE = None
# If set to True, existing persistent database connections will be health checked,
# before they are reused in each request performing database access.
# If the health check fails, the connection will be reestablished without failing the request,
# when the connection is no longer usable but the database server is ready to accept
# and serve new connections (e.g. after database server restart closing existing connections).
CONN_HEALTH_CHECKS = True

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIR = []
STATIC_ROOT = "{base_dir}/static".format(base_dir=BASE_DIR)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Use nose to run all tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

NOSE_ARGS = ["--cover-package=construction_work"]
