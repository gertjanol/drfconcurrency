from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE, ISOLATION_LEVEL_REPEATABLE_READ

SECRET_KEY = 'dmzyql+1uz-9f3eb^ns3cj!#b6p(kb2cw!6lwg+z=-o9+1w8z*'
DEBUG = False
ALLOWED_HOSTS = ['*']

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
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
        # 'ATOMIC_REQUESTS': True,
        # 'OPTIONS': {
        #     'isolation_level': ISOLATION_LEVEL_SERIALIZABLE,
        # },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False
    }
}
