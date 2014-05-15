from django.conf.urls import patterns, url
from views import AlteregosCreateView, AlteregosDetailView, AlteregosUpdateView, AlteregosDeleteView, AlteregosListView,\
    PowerCreateView

urlpatterns = patterns('',

    url(r'^hero-add/$', AlteregosCreateView.as_view(), name='create'),
    url(r'^power-add/$', PowerCreateView.as_view(), name='power_create'),

    url(r'^(?P<pk>[\w\d]+)/$', AlteregosDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w\d]+)/edit/$', AlteregosUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[\w\d]+)/delete/$', AlteregosDeleteView.as_view(), name='delete'),

    url(r'^$', AlteregosListView.as_view(), name='list'),

)
urlpatterns += patterns('',
    url(r'^gridfs/(?P<file_id>[0-9a-f]{24})/$', 'superheroes.views.serve_file', name='image'),
)
