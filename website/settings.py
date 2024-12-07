"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.getenv("RENDER_EXTERNAL_HOSTNAME","")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [

            os.path.join(BASE_DIR,'core/registeration/templates') , ### registeration page templates path

            os.path.join(BASE_DIR,'core/ui/templates') , ### ui pages templates path 
        ],
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

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


### My edits 


INSTALLED_APPS += [
    'core',
]

AUTH_USER_MODEL = 'core.User'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/registeration/static'), ## login page static folder path 

    os.path.join(BASE_DIR,'core/ui/static') ## ui page static folder 
]

### whitenoise install

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"




LOGIN_URL = 'login'

### adding rest frame work for django

INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  
        'rest_framework.authentication.SessionAuthentication',  
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


### LLM API configs

LLM_API_KEY = os.environ.get('LLM_API_KEY')

LLM_API_URL = 'https://api.cohere.ai/v1/chat'

LLM_MODEL = 'command-r-08-2024'

TAG_LIST = [
    "Technology", "Science", "Innovation", "Research", "Education", 
    "Artificial Intelligence (AI)", "Machine Learning", "Quantum Computing", 
    "Robotics", "Space Exploration", "Microbiology", "Biotechnology", 
    "Genetics", "Medicine", "Health Tech", "Mental Health", "Nutrition", 
    "Fitness", "Wellness", "Environmental Science", "Travel", "Food", 
    "Sustainability", "Personal Development", "Productivity", "Creativity", 
    "Minimalism", "Fashion", "Photography", "Writing", "Entrepreneurship", 
    "Startups", "E-commerce", "Digital Marketing", "Blockchain", 
    "Cryptocurrency", "Fintech", "Leadership", "Economics", "Investments", 
    "Web Development", "Software Engineering", "Python", "JavaScript", 
    "Data Science", "Cybersecurity", "Open Source", "DevOps", 
    "Internet of Things (IoT)", "Cloud Computing","Junk","Random","Personal","Test"
]

LLM_PRE_PROMPT = f'can you characterize the given input by assign them atmost five tags from the following tags list. And return the output just tags seperated by comman nothing else. Tags List: {str(TAG_LIST)}',


### defining the database 

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('db_name'),
#         'USER': os.environ.get('db_user'),
#         'PASSWORD': os.environ.get('db_password'),
#         'HOST': 'localhost',  # Use '127.0.0.1' if needed
#         'PORT': '5432',       # Default PostgreSQL port
#     }
# }

import dj_database_url


DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'),conn_max_age=600)
}


### ssl and tsl

if "test" not in sys.argv and False:

    SECURE_HSTS_SECONDS = 31536000  # Enable HTTP Strict Transport Security
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


