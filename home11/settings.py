from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = 'dev-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'app',  
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  
        'APP_DIRS': True,  
        'OPTIONS': {
            'context_processors': [],
        },
    },
]

STATIC_URL = "/static/"
