"""
Django settings for the Hostel Management SaaS backend.

All secrets/config are read from environment variables. See .env.example.
"""

from datetime import timedelta
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DJANGO_DEBUG=(bool, False),
)


# Load .env from project root
environ.Env.read_env(
    str(BASE_DIR.parent / ".env")
)


# -------------------------------------------------
# Core Django Settings
# -------------------------------------------------

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="insecure-dev-key-do-not-use-in-prod"
)


DEBUG = env(
    "DJANGO_DEBUG",
    default=False
)


ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "testserver",
        "192.168.100.2",
    ],
)



# -------------------------------------------------
# Applications
# -------------------------------------------------

INSTALLED_APPS = [

    "django.contrib.admin",

    "django.contrib.auth",

    "django.contrib.contenttypes",

    "django.contrib.sessions",

    "django.contrib.messages",

    "django.contrib.staticfiles",


    # Third party

    "rest_framework",

    "rest_framework_simplejwt",

    "rest_framework_simplejwt.token_blacklist",

    "django_filters",

    "corsheaders",


    # Local apps

    "apps.accounts",

    "apps.tenants",

    "apps.hostels",

    "apps.rooms",

    "apps.beds",

    "apps.expenses",

    "apps.tenant_profiles",

    "apps.bookings",

    "apps.payments",

    "apps.attendance",

    "apps.visitors",

    "apps.complaints",

    "apps.staff",

    "apps.inventory",
]



# -------------------------------------------------
# Middleware
# -------------------------------------------------

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",


    # SaaS tenant isolation

    "middleware.tenant.TenantContextMiddleware",
]



ROOT_URLCONF = "config.urls"



# -------------------------------------------------
# Templates
# -------------------------------------------------

TEMPLATES = [

    {

        "BACKEND":
        "django.template.backends.django.DjangoTemplates",


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



WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"




# -------------------------------------------------
# Database
# -------------------------------------------------

DATABASES = {

    "default": {

        "ENGINE":
        "django.db.backends.postgresql",


        "NAME":
        env(
            "POSTGRES_DB",
            default="hostel_saas"
        ),


        "USER":
        env(
            "POSTGRES_USER",
            default="hostel_saas_user"
        ),


        "PASSWORD":
        env(
            "POSTGRES_PASSWORD",
            default=""
        ),


        "HOST":
        env(
            "POSTGRES_HOST",
            default="localhost"
        ),


        "PORT":
        env(
            "POSTGRES_PORT",
            default="5432"
        ),

    }

}


# -------------------------------------------------
# Authentication
# -------------------------------------------------

AUTH_USER_MODEL = "accounts.User"



AUTH_PASSWORD_VALIDATORS = [

    {

        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"

    },


    {

        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",

        "OPTIONS": {

            "min_length": 10

        }

    },


    {

        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"

    },


    {

        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"

    },

]




# -------------------------------------------------
# Localization
# -------------------------------------------------

LANGUAGE_CODE = "en-us"


TIME_ZONE = "UTC"


USE_I18N = True


USE_TZ = True




# -------------------------------------------------
# Static / Media
# -------------------------------------------------

STATIC_URL = "/static/"


STATIC_ROOT = BASE_DIR / "staticfiles"



MEDIA_URL = "/media/"


MEDIA_ROOT = BASE_DIR / "media"



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"





# -------------------------------------------------
# Django REST Framework
# -------------------------------------------------

REST_FRAMEWORK = {


    "DEFAULT_AUTHENTICATION_CLASSES": (

        "rest_framework_simplejwt.authentication.JWTAuthentication",

    ),



    "DEFAULT_PERMISSION_CLASSES": (

        "rest_framework.permissions.IsAuthenticated",

    ),



    "DEFAULT_FILTER_BACKENDS": (

        "django_filters.rest_framework.DjangoFilterBackend",

    ),



    "DEFAULT_PAGINATION_CLASS":

        "rest_framework.pagination.PageNumberPagination",



    "PAGE_SIZE": 25,



    "DEFAULT_THROTTLE_CLASSES": [

        "rest_framework.throttling.ScopedRateThrottle",

    ],



    "DEFAULT_THROTTLE_RATES": {

        "auth": "10/min",

    },

}




# -------------------------------------------------
# JWT
# -------------------------------------------------

SIMPLE_JWT = {


    "ACCESS_TOKEN_LIFETIME":

        timedelta(

            minutes=env.int(

                "ACCESS_TOKEN_LIFETIME_MINUTES",

                default=15

            )

        ),



    "REFRESH_TOKEN_LIFETIME":

        timedelta(

            days=env.int(

                "REFRESH_TOKEN_LIFETIME_DAYS",

                default=7

            )

        ),



    "ROTATE_REFRESH_TOKENS": True,



    "BLACKLIST_AFTER_ROTATION": True,



    "UPDATE_LAST_LOGIN": True,

}





# -------------------------------------------------
# CORS
# -------------------------------------------------

CORS_ALLOWED_ORIGINS = [

    # Local development
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://192.168.100.2:5173",

    # Production frontend
    "https://traversedw.com.np",
]



CORS_ALLOW_CREDENTIALS = True



CORS_ALLOW_HEADERS = [


    "accept",


    "accept-encoding",


    "authorization",


    "content-type",


    "dnt",


    "origin",


    "user-agent",

]



CSRF_TRUSTED_ORIGINS = [

    # Local development
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.100.2:5173",

    # Production frontend
    "https://traversedw.com.np",
]

# -------------------------------------------------
# Celery
# -------------------------------------------------

CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL",
    default="redis://localhost:6379/0"
)


CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND",
    default="redis://localhost:6379/0"
)





# -------------------------------------------------
# Frontend URL
# -------------------------------------------------

FRONTEND_URL = env(
    "FRONTEND_URL",
    default="http://localhost:5173"
)





# -------------------------------------------------
# Email Configuration
# -------------------------------------------------

EMAIL_BACKEND = env(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend"
)



EMAIL_HOST = env(
    "EMAIL_HOST",
    default="smtp.gmail.com"
)



EMAIL_PORT = env.int(
    "EMAIL_PORT",
    default=587
)



EMAIL_USE_TLS = env.bool(
    "EMAIL_USE_TLS",
    default=True
)



EMAIL_USE_SSL = env.bool(
    "EMAIL_USE_SSL",
    default=False
)



EMAIL_HOST_USER = env(
    "EMAIL_HOST_USER",
    default=""
)



EMAIL_HOST_PASSWORD = env(
    "EMAIL_HOST_PASSWORD",
    default=""
)



DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="Nestled Hostel <noreply@example.com>"
)



SERVER_EMAIL = DEFAULT_FROM_EMAIL





# -------------------------------------------------
# Logging
# -------------------------------------------------

LOGGING = {

    "version": 1,


    "disable_existing_loggers": False,



    "formatters": {


        "verbose": {

            "format":
            "[{asctime}] {levelname} {name}: {message}",

            "style": "{",

        },

    },



    "handlers": {


        "console": {

            "class":
            "logging.StreamHandler",

            "formatter":
            "verbose",

        },

    },



    "root": {


        "handlers": [

            "console"

        ],


        "level":

        "INFO",

    },



    "loggers": {


        "django": {


            "handlers": [

                "console"

            ],


            "level":

            "INFO",


            "propagate":

            False,

        },



        "apps": {


            "handlers": [

                "console"

            ],


            "level":

            "INFO",


            "propagate":

            False,

        },

    },

}

