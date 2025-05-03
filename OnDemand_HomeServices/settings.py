# On top of settings.py
import os
from pathlib import Path
import dj_database_url

# 1) Define BASE_DIR first
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) Secret & debug via env
SECRET_KEY = os.environ.get('SECRET_KEY', '<your‑dev‑secret‑here>')
DEBUG      = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# 3) Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',   # ← your app
]

# 4) Middleware (note WhiteNoise for static files)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OnDemand_HomeServices.urls'       # ← match your project folder
WSGI_APPLICATION = 'OnDemand_HomeServices.wsgi.application'

# 5) Templates
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [ BASE_DIR / 'templates' ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# 6) Database: use dj_database_url to parse DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# 7) Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'
USE_I18N      = True
USE_TZ        = True

# 8) Static files
STATIC_URL         = '/static/'
STATIC_ROOT        = BASE_DIR / 'staticfiles'
STATICFILES_DIRS   = [ BASE_DIR / 'static' ]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 9) Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
