import os
from pathlib import Path
import dj_database_url
from envparse import env
from settings_pd import Settings_TDL


setings_bs = Settings_TDL()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = setings_bs.DJ_SECRET_KEY
DEBUG = setings_bs.DJ_DEBUG

ALLOWED_HOSTS =['localhost', '127.0.0.1', '[::1]', '0.0.0.0','bityutskiyna-skypro-td.space']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_filters',
    'django.contrib.staticfiles',
    'social_django',
    'rest_framework',
    'core',
    'goals',
    'bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todolist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'todolist.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': setings_bs.POSTGRES_DB,
        'USER': setings_bs.POSTGRES_USER,
        'PASSWORD': setings_bs.POSTGRES_PASSWORD,
        'HOST': setings_bs.DB_HOST,
        'PORT': setings_bs.DB_PORT,
    }
}
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'core.User'

STATIC_URL = 'static/'

CSRF_COOKIE_SECURE = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
)

SOCIAL_AUTH_VK_OAUTH2_KEY = setings_bs.SOCIAL_AUTH_VK_OAUTH2_KEY
SOCIAL_AUTH_VK_OAUTH2_SECRET = setings_bs.SOCIAL_AUTH_VK_OAUTH2_SECRET
SOCIAL_AUTH_LOGIN_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL  = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL ='/login-error/'
SOCIAL_AUTH_VK_OAUTH2_SCOPE=['email']
SOCIAL_AUTH_VK_EXTRA_DATA=[('email','email')]
SOCIAL_AUTH_NEW_USER_REDIRECT_URL='/logged-in/'
SOCIAL_AUTH_USER_MODEL='core.User'

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE':10
}
BOT_TOKEN = setings_bs.BOT_TOKEN