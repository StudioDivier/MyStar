"""
Django settings for MyStar project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from . import config
from .config import OAUTHDATA
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.sk

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# '192.168.1.131'
ALLOWED_HOSTS = ['192.168.1.131', '127.0.0.1']
SITE_ID = 1
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640


# Application definition

INSTALLED_APPS = [
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    # Core
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'django_rest_passwordreset',
    'yandex_checkout',

    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    # Apps
    'users',
]

AUTH_USER_MODEL = 'users.Users'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.backends.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',

    ),
    # 'EXCEPTION_HANDLER': 'django_rest_logger.handlers.rest_exception_handler',
}

AUTHENTICATION_BACKENDS = (
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',

    # facebook
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

    #  google
    'social_core.backends.google.GoogleOAuth2',
    # vk
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.vk.VKAppOAuth2',
    # yandex
    'social_core.backends.yandex.YandexOAuth2',
    # mail
    'social_core.backends.mailru.MailruOAuth2',
    # OK
    'social_core.backends.odnoklassniki.OdnoklassnikiOAuth2',

    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

REST_USE_JWT = True


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

APPEND_SLASH = False

ROOT_URLCONF = 'MyStar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
        },
    },
]

WSGI_APPLICATION = 'MyStar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# PostgreSQL 10.14

DATABASES = config.data



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
CORS_ORIGIN_ALLOW_ALL = True

LANGUAGE_CODE = 'ru-RU'

LANGUAGES = [
    ('ru', ('Russian')),

]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

if DEBUG:
    STATIC_URL = os.path.join(BASE_DIR, '/STATIC/DEV/static/')
    STATIC_ROOT = os.path.join(BASE_DIR, 'STATICFILES/DEV')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
    AVATAR_ROOT = os.path.join(BASE_DIR, 'media/avatars/')
    VIDEO_ROOT = os.path.join(BASE_DIR, 'media/videos/')
    MEDIA_URL = '/media/'
else:
    STATIC_URL = '/static/'
    MEIDA_ROOT = os.path.join(BASE_DIR, 'media')


# data for mailing service
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.hosting.reg.ru'
EMAIL_PORT = '587'
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# yandex kassa

# oAuth2
# vk data
SOCIAL_AUTH_VK_OAUTH2_KEY = OAUTHDATA.SOCIAL_AUTH_VK_OAUTH2_KEY
SOCIAL_AUTH_VK_OAUTH2_SECRET = OAUTHDATA.SOCIAL_AUTH_VK_OAUTH2_SECRET
# google data
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = OAUTHDATA.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = OAUTHDATA.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
# fb data
SOCIAL_AUTH_FB_OAUTH2_KEY = OAUTHDATA.SOCIAL_AUTH_FB_OAUTH2_KEY
SOCIAL_AUTH_FB_OAUTH2_SECRET = OAUTHDATA.SOCIAL_AUTH_FB_OAUTH2_SECRET
# instagram data

# yandex data
SOCIAL_AUTH_YANDEX_OAUTH2_KEY = OAUTHDATA.SOCIAL_AUTH_YANDEX_OAUTH2_KEY
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = OAUTHDATA.SOCIAL_AUTH_YANDEX_OAUTH2_SECRET
# mail data
SOCIAL_AUTH_MAIL_OAUTH2_KEY = OAUTHDATA.SOCIAL_AUTH_MAIL_OAUTH2_KEY
SOCIAL_AUTH_MAIL_OAUTH2_SECRET = OAUTHDATA.SOCIAL_AUTH_MAIL_OAUTH2_SECRET
# ok data
SOCIAL_AUTH_OK_OAUTH2_KEY = OAUTHDATA.SOCIAL_AUTH_OK_OAUTH2_KEY
SOCIAL_AUTH_OK_OAUTH2_SECRET = OAUTHDATA.SOCIAL_AUTH_OK_OAUTH2_SECRET

LOG_PATH = os.path.join(BASE_DIR, "log/")
# file ------> Writes logs to file
# console ---> Prints logs in console
DRF_LOGGER_HANDLER = ["file", "console"]

# Log file directory
# Make sure directory exists
DRF_LOGGER_FILE = LOG_PATH + 'custom_logger.log'
