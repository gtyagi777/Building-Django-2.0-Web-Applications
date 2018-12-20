from config.settings.common_settings import *

DEBUG = True
SECRET_KEY = 'some key'

INSTALLED_APPS += [
    'debug_toolbar'
]

# Database configuration
DATABASES['default'].update({
    'NAME': 'mymdb',
    'USER': 'mymdb',
    'PASSWORD': 'development',
    'HOST': 'localhost',
    'PORT': 5432
})

# Caches
CASHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': 5, # 5 seconds
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, '../media_root')


# Django debug toolbar
INTERNAL_IPS = [
    '127.0.0.1'
]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE