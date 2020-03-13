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
        'ENGINE':   'django.contrib.gis.db.backends.postgis',
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

DATABASE_ROUTERS = []  # turn off second database
SLAVE_DATABASES = []

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1']

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True
CHECK_EXPIRED_TEMP_TOKEN = False

# pylint: disable=simplifiable-if-statement
if len(sys.argv) >= 2 and (sys.argv[1] == "test" or sys.argv[1] == "test_all"):
    # This trick works only when we run tests from the command line.
    TESTING_MODE = True
else:
    TESTING_MODE = False

CELERY_BROKER_URL = 'amqp://guest:@queue:5672//'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_CACHE_BACKEND = 'memory'
CELERY_BROKER_CONNECTION_MAX_RETRIES = 2

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')  # noqa

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_STORAGE_BUCKET_NAME=os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_BUCKET_ACL=None
AWS_DEFAULT_ACL=None
