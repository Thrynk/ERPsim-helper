# Django settings for docs project.
# import source code dir
import os
import sys
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), os.pardir))

SITE_ID = 303
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DATABASES = {
    "default": {
        "NAME": ":memory:",
        "ENGINE": "django.db.backends.sqlite3",
        "USER": '',
        "PASSWORD": '',
        "PORT": '',
    }
}

INSTALLED_APPS = (
    'erpsim_helper.apps.ErpsimHelperConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'huey.contrib.djhuey',
)

# settings.py
HUEY = {
    'name': 'my-app',
    'huey_class': 'huey.MemoryHuey',

    # To run Huey in "immediate" mode with a live storage API, specify
    # immediate_use_memory=False.
    'immediate_use_memory': False,
}