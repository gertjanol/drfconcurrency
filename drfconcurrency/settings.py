import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'dmzyql+1uz-9f3eb^ns3cj!#b6p(kb2cw!6lwg+z=-o9+1w8z*'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',

    'concur.apps.ConcurConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'drfconcurrency.urls'
WSGI_APPLICATION = 'drfconcurrency.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'default.db'),
    }
}
