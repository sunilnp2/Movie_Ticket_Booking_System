"""
Django settings for qfxcinema project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# templates and static directory

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')



# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cinema',
    'authentication',
    'movie',
    'booking',
    'utils',
    'rest_framework',  
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
]

ROOT_URLCONF = 'qfxcinema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'qfxcinema.wsgi.application'
STATICFILES_DIRS = [STATIC_DIR]


LOGIN_URL = 'authentication:login'
# LOGIN_REDIRECT_URL = 'booking:seat'
LOGOUT_REDIRECT_URL = 'cinema:home'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#    'default': {
#        'ENGINE': config('ENGINE'),
#        'NAME': config('NAME'),
#        'USER': config('USER'),
#        'PASSWORD': config('PASSWORD'),
#        'HOST': config('HOST'),
#        'PORT': config('PORT',default=5432, cast=int),
#    }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'qfxcinema',
       'USER': 'postgres',
       'PASSWORD': 'postgres',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Emailing settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'nepalisun22@gmail.com'
EMAIL_HOST_USER = 'nepalisun22@gmail.com'
EMAIL_HOST_PASSWORD = 'bqzirddspkhlrfpm'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PASSWORD_RESET_TIMEOUT = 14400

# EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_FROM = config('EMAIL_FROM')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = config('EMAIL_PORT')
# EMAIL_USE_TLS = True

# PASSWORD_RESET_TIMEOUT = 14400


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'authentication.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRONJOBS = [
    ('*/3 * * * *', 'cinema.cron.DeleteUnverifiedAccount')
]



# Celery settings
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379"
CELERY_ACCEPT_CONTENT = ['application/json'] 
CELERY_RESULT_SERIALIZER = 'json' 
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kathmandu'



# -------------------------------------Rest Framework------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}


# Django project settings.py
from datetime import timedelta
from django.conf import settings

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}



# cors headers -------------------------------------------------
CORS_ALLOW_CREDENTIALS = True 
CSRF_COOKIE_SECURE = False
CORS_ALLOW_ALL_ORIGINS = True


# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     'http://localhost:8000',
#     # Add other allowed origins if needed
# ]
# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:8000",
#     'http://localhost:8000',
# ]
# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "localhost",
# ]
# CORS_ORIGIN_WHITELIST = [
#      "http://127.0.0.1:8000",
#      'http://localhost:8000',
# ]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    # Add other allowed origins if needed
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
]
# ALLOWED_HOSTS = [
#     'localhost',
# ]
ALLOWED_HOSTS = ['localhost']

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Charset',
    'Accept-Encoding',
    'Content-Type',
    'DNT',
    'Origin',
    'User-Agent',
    'X-Requested-With',
    'Accept-Language',
    'Authorization',
    'contentType', 
    'x-csrftoken'
]



# django filters


# -------------------------------Django Loggers----------------------------------

# LOGGING = {
#     'version': 1,
#     # The version number of our log
#     'disable_existing_loggers': False,
#     # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
#     # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
#     'handlers': {
#         'file': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'info.log',
#         },
#     },
#     # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
#     'loggers': {
#        # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
#         '': {
#             'handlers': ['file'], #notice how file variable is called in handler which has been defined above
#             'level': 'WARNING',
#             'propagate': True,
#         },
#     },
# }


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }



import os

# Define the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
   
    'formatters': {
    'verbose': {
        'format': '{levelname} {asctime} {module} {lineno} {message}',
        'style': '{'
    },
    'error_verbose': {
        'format': '{levelname} {asctime} {module} {lineno} {message}\n{error}',
        'style': '{'
    },
},

 'handlers': {
        'file': {
            'level': 'DEBUG',  # Change to WARNING level
            'class': 'logging.FileHandler',
            'formatter':'verbose',
            'filename': os.path.join(BASE_DIR, 'info.log'),  # Change the filename
        },
    },

    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',  # Change to DEBUG to capture all levels
            'propagate': True,
        },
    },
}


#--------------------------------pyest--------------------
# import os
# import pytest
# from django.conf import settings

# # Configure Django settings for testing
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qfxcinema.settings')
# settings.configure()
