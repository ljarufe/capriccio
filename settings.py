# Django settings for capriccio project.
import os
from os.path import dirname
basedir = dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql',
        'NAME': 'capriccio',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'juarez',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-pe'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s/media/' % basedir

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1nkh=uj$ojn8gl2unlp0j9q(7xu0+)%vuh9dc78!i#%0xeh=ni'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


#TEMPLATE_CONTEXT_PROCESSORS = (
     #'django.contrib.auth.context_processors.auth',
     #'django.core.context_processors.auth',
     #'messages.context_processors.inbox',
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'projectcapriccio.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'django.template.loaders.app_directories.load_template_source',
    '/%s/templates/' % basedir,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.admin',
    # capriccio apps
    'projectcapriccio.clientes',
    'projectcapriccio.common',
    'projectcapriccio.common.templatetags.commontags',
    'projectcapriccio.ventas',
    'projectcapriccio.empresa',
    'projectcapriccio.notificaciones',    
    'projectcapriccio.admin',
    'projectcapriccio.paginas',
    # utils
    'projectcapriccio.sorl.thumbnail',
    #'gdata',
    'projectcapriccio.atom',
    'projectcapriccio.notification',
)

#Items por pagina
ITEMS_PAGINA = 8
# Modelo para usuario
AUTH_PROFILE_MODULE = "common.Usuario"
#api de google maps
MAPS_API_KEY = 'XZVFJJKK'
# Opciones para el envio de emails desde el servidor

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'aqpnet'
EMAIL_HOST_PASSWORD = '04718802'
EMAIL_PORT = 587
#EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "systems@capriccioperu.com"
SERVER_EMAIL = "systems@capriccioperu.com"
CHECKOUT_ID = "1420806"
CACHE_BACKEND = 'db://cachetable/?timeout=30&max_entries=80'
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
