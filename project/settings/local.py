from .base import *

STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'