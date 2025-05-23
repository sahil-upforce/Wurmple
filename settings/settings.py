from datetime import timedelta

from settings import ENV_VARIABLES

SECRET_KEY = ENV_VARIABLES.get("SECRET_KEY", "is-not-used")
DEBUG = ENV_VARIABLES.get("DEBUG", False)
ALLOWED_HOSTS = ENV_VARIABLES.get("DJANGO_ALLOWED_HOSTS", "*").split(" ")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Location
    "django.contrib.gis",
    # Third Party
    "django_celery_results",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt",
    "phone_field",
    # Project APPs
    "core",
    "user_app",
    "tour_management",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "templates",
        ],
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

ROOT_URLCONF = "Wurmple.urls"

WSGI_APPLICATION = "Wurmple.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": ENV_VARIABLES["DB_NAME"],
        "USER": ENV_VARIABLES["DB_USER"],
        "PASSWORD": ENV_VARIABLES["DB_PASSWORD"],
        "HOST": ENV_VARIABLES["DB_HOST"],
        "PORT": ENV_VARIABLES["DB_PORT"],
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

STATIC_URL = "/static/"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user_app.User"

AUTHENTICATION_BACKENDS = ["user_app.backends.UserAndEmailBackend"]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "USER_ID_FIELD": "public_id",
}

REDIS_HOST = ENV_VARIABLES.get("REDIS_HOST", "localhost")
REDIS_PORT = ENV_VARIABLES.get("REDIS_PORT", 6379)

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = "UTC"

GDAL_LIBRARY_PATH = "/opt/homebrew/Cellar/gdal/3.8.4_2/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/opt/homebrew/Cellar/geos/3.12.1/lib/libgeos_c.dylib"
