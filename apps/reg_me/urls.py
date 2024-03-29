from django.conf.urls import patterns, url


urlpatterns = patterns('reg_me.views',
    url('register/', 'register', {}, 'register'),
    url('registered/', 'registered', {}, 'registered'),
    url('activate/(?P<username>\w+)/(?P<activation_key>\w+)',
        'activate', {}, 'activate'),
    url('activated/', 'activated', {}, 'activated'),
)
