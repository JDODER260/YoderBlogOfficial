import os
from pathlib import Path

DEBUG = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_xtf+fa)xrahub)#kolq5!g!@f44b5+m!l$!c(%j7^(2z=zz$j'

# SECURITY WARNING: don't run with debug turned on in production!

CKEDITOR_CONFIGS = {
    'default': {
        'height': '35%',
        'width': 'full',
    },
}

ALLOWED_HOSTS = [
    '127.0.0.1',
    'a3efe492-e1e5-47bc-8295-4bc058d46775.id.repl.co', '10.10.3.154',
    'jdswebsites.xyz', 'jdswebsites.xyz', 'localhost', 'yoder-blog--yoder-blog.repl.co',
    '10.10.3.169:16798', '10.10.3.124', '10.30.2.48', '10.10.3.148',
    "yoder-blog.repl.co", "dfd1c7d6-7812-4b88-b31f-7d8927f11ce6.id.repl.co", "127.0.0.1"
]

CSRF_TRUSTED_ORIGINS = [
    'https://a3efe492-e1e5-47bc-8295-4bc058d46775.id.repl.co',
    'https://yoderblog.projectnpj.repl.co', 'https://jdswebsites.xyz',
    'http://127.0.0.1:8000', "https://yoder-blog.repl.co"
]

# Application definition

INSTALLED_APPS = [
    'ckeditor',
    'crispy_forms',
    'users.apps.UsersConfig',
    'main.apps.MainConfig',
    'chat.apps.ChatConfig',
    'post.apps.PostConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'crispy_bootstrap4',
]
CSRF_COOKIE_SECURE = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mysite.middleware.RateLimitMiddleware',
    'mysite.middleware.UpdateIPMiddleware',
    #'mysite.middleware.UnderMaintenanceMiddleware',
]

MIDDLEWARE_CLASSES = (
    'mysite.middleware.UpdateLastActiveMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
CRISPY_TEMPLATE_PACK = 'bootstrap4'
#Location of static files
#STATIC_ROOT  = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'blog-home'

LOGIN_URL = 'login'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

LOGOUT_REDIRECT_URL = 'blog-home'
