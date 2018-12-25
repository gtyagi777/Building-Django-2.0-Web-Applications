from config.common_settings import *

DEBUG = True
SECRET_KEY = 'some secret'

DATABASES['default'].update({
    'NAME': 'answerly',
    'USER': 'answerly',
    'PASSWORD': 'development',
    'HOST': '127.0.0.1',
    'PORT': '5432'
})