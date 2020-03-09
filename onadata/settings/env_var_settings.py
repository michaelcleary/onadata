# flake8: noqa
from onadata.settings.common import *

# this setting file will not work on "runserver" -- it needs a server for
# static files
DEBUG = False

# override to set the actual location for the production static and media
# directories
MEDIA_ROOT = '/var/formhub-media'
STATIC_ROOT = "/srv/formhub-static"
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static"),
)
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
# your actual production settings go here...,.
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ['FORMHUB_DB_NAME'],
        'USER':     os.environ['FORMHUB_DB_USER'],
        # the password must be stored in an environment variable
        'PASSWORD': os.environ['FORMHUB_DB_PASSWORD'],
        # the server name may be in env
        'HOST':     os.environ.get("FORMHUB_DB_SERVER", 'dbserver.yourdomain.org')
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = os.environ.get('FORMHUB_TZ', 'Africa/Lagos')

TOUCHFORMS_URL = 'http://localhost:9000/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['FORMHUB_SECRET']

