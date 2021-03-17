import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# If value of environment variable DEBUG is "True", it gets evaluated as boolean True
DEBUG = os.getenv('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')


# Application definition

INSTALLED_APPS = [
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',
    'users',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'tinymce',
    'crispy_forms',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Different database configurations, if on github or other environment
if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github-actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('SQL_DATABASE'),
            'USER': os.getenv('SQL_USER'),
            'PASSWORD': os.getenv('SQL_PASSWORD'),
            'HOST': os.getenv('SQL_HOST'),
            'PORT': os.getenv('SQL_PORT'),
        }
    }


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Path to venv
VENV_PATH = os.path.dirname(BASE_DIR)

# Path for collectstatic to store files
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')


# User uploaded files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(VENV_PATH, 'media_root')

# For crispy formats
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Redirect to home URL after login/logout (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# For django.contrib.sites
SITE_ID = 1

# For AWS S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# Will append extra chracters to prevent overwrite
AWS_S3_FILE_OVERWRITE = True

STATIC_URL = 'static/'

# Configuration used by django-storages

# To upload your media files to S3
DEFAULT_FILE_STORAGE = 'blog.s3_storages.MediaStorage'

# If in production environment, activate s3 storage for static files
if not DEBUG:
    # To allow django-admin collectstatic to automatically put your static files in your bucket
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    # Base location for static files stores in S3
    STATIC_URL = 'https://eduardo-blog.s3-sa-east-1.amazonaws.com/'

# Directory where uploaded files will be saved
MEDIAFILES_LOCATION = 'uploads'

# A path prefix that will be prepended to all uploads
AWS_LOCATION = 'static'

FILEBROWSER_DEFAULT_PERMISSIONS = None

# Speeds up the load of the filebrowser files
FILEBROWSER_LIST_PER_PAGE = 5
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

# For tinymce
TINYMCE_DEFAULT_CONFIG = {

    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'width': '100%',
    'plugins': '''
            autoresize textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            preview bold italic underline | fontselect,
            fontsizeselect  | forecolor | alignleft alignright |
            aligncenter alignjustify | bullist numlist table |
            | link image media | codesample | hr code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    }

# Heroku: Update database configuration from $DATABASE_URL.
# If IS_HEROKU is 'True', use Heroku's database
IS_HEROKU = os.getenv('IS_HEROKU')
if IS_HEROKU == 'True':
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
