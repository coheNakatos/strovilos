"""

Django settings for strovilos project.

"""
import os
from .secret_settings import *
from django.utils.translation import ugettext_lazy as _

########################################################################################################
######################################## Basic/Custom Settings #########################################
########################################################################################################
#TODO: DEBUG / EMAIL BACKEND / COMPRESS

# Custom Variables 
POSTS_PER_PAGE = 10
TITLE_COUNT = 10
DESC_COUNT = 28

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Virtualenv DIR
ROOT_DIR = os.path.dirname(BASE_DIR)

# Static files (CSS, JavaScript, Images)
# ROOT paths are set in secret_settings
STATIC_URL = '/static/'
MEDIA_URL = '/media/'


DEBUG = True
if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['strovilos.gr','www.strovilos.gr']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'grappelli',
    'django.contrib.admin',
    'ckeditor_uploader',
    'ckeditor',
    'django_batch_uploader',
    'huey.contrib.djhuey',
    'compressor',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.AdminLocaleURLMiddleware',
    'login_failure.middleware.RequestProvider',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'main.context_processors.global_settings',
		        'django.core.context_processors.request',
            ],
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

ROOT_URLCONF = 'strovilos.urls'
WSGI_APPLICATION = 'strovilos.wsgi.application'


# Password validation

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


# Cache Settings

CACHE_PREFIX = 'PostViews_'
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:'+ CACHE_PASSWORD +'@localhost:6379',
        'OPTIONS': {
            'CLIENT_CLASS' : 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}


# Logging Settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(module)s.py:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'WARN',
            'class': 'logging.FileHandler',
            'filename': os.path.join(ROOT_DIR, 'log/debug.log'),
            'formatter' : 'standard',
        },
        'fail2ban_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(ROOT_DIR, 'log/fail2ban.log'),
            'formatter' : 'standard',
        },
        'huey_file': {
            'level': 'WARN',
        'class': 'logging.FileHandler',
            'filename': os.path.join(ROOT_DIR, 'log/huey_debug.log'),
            'formatter' : 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'WARN',
            'propagate': False,
        },
        'main' : {
            'handlers': ['file'],
            'level' : 'WARN',
        },
        'huey.consumer': {
            'handlers': ['huey_file'],
            'level': 'WARN',
            'propagate': True,
       },
       'fail2ban': {
            'handlers': ['fail2ban_file'],
            'level': 'ERROR',
       }
    },
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = None 

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = (
    ('el', _('Greek')),
    ('en', _('English')),
)
ADMIN_LANGUAGE_CODE = 'el'

########################################################################################################
######################################## Installed Apps Settings #######################################
########################################################################################################

# Compress 
COMPRESS_ENABLED = False if DEBUG else True

COMPRESS_CSS_FILTERS = [
	'compressor.filters.css_default.CssAbsoluteFilter',
	'compressor.filters.cssmin.rCSSMinFilter',
]

# Email Agent Setup

# Uncomment this for testing
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_USER = 'linosgian'
DEFAULT_FROM_EMAIL = SENDGRID_USER + '@sendgrip.com'
DEFAULT_TO_EMAIL = 'kgstrovilos@gmail.com'

# Huey Consumer

HUEY = {
    'name': 'main',
    'connection' : { 'password' : CACHE_PASSWORD,},
    'consumer': {'workers': 1, 'worker_type': 'thread'},
}

# Grappeli  

# Enable this to switch between users in admin
# GRAPPELLI_SWITCH_USER = True
GRAPPELLI_ADMIN_TITLE = 'Επεξεργασία Ιστοσελίδας'

# CKEditor 

CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "images/"
CKEDITOR_CONFIGS = {
    
    'default': {
        'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'tools', 'items': ['Maximize']}, 
            {'name': 'clipboard', 'items': ['PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace' ]},
            '/',
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote',  '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'Image', 'Link', 'Unlink', 'Anchor', 'HorizontalRule' ]},
            '/',
            {'name': 'styles', 'items': ['Bold', 'Italic', 'Underline', 'RemoveFormat', 'Styles', 'Format', 'Font', 'FontSize', 'Centerizer']},
        ],
        'toolbar': 'YourCustomToolbarConfig',
         'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
         'height': 291,
         'width': 800,
         'filebrowserWindowHeight': 725,
         'filebrowserWindowWidth': 940,
         'toolbarCanCollapse': True,
         'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                #'autogrow',
                #'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath',
                'wordcount',
                'centerizer',
            ]),
        'removePlugins': 'smiley',
        'disableNativeSpellChecker' : False,
    }
}
