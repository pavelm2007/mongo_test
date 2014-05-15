from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^accounts/', include('account.urls')),
                       url(r'^registration/', include('reg_me.urls')),
                       url(r'^', include('superheroes.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)