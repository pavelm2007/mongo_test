from django.conf.urls import patterns, url

# from .views import LoginView

urlpatterns = patterns('',
                       url('login.html', 'account.views.login_view', {}, 'login'),
                       url('logout.html', 'django.contrib.auth.views.logout',  {'template_name': 'account/login.html'}, 'logout'),

                       # url('login.html', LoginView.as_view(), {}, 'login'),
)
