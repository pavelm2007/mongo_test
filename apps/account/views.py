import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME, login

from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth import login as django_login

from mongoengine.django.auth import MongoEngineBackend

from .forms import AccountLoginForm
from django.contrib.auth import login as django_login
from forms import AuthenticationForm

from django.shortcuts import redirect, render_to_response, RequestContext


def login_view(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        backend = MongoEngineBackend()
        user = backend.authenticate(username=request.POST['username'], password=request.POST['password'])
        # print user.get_user()
        django_login(request, user)

        return redirect('list')
    else:
        #     except DoesNotExist:
        #         return HttpResponse('user does not exist')
        # else:
        #     form = AuthenticationForm()
        #
        return render_to_response('account/login.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.

    Usage:
        in urls.py:
            url(r'^login/$',
                AuthenticationView.as_view(
                    form_class=MyCustomAuthFormClass,
                    success_url='/my/custom/success/url/),
                name="login"),

    """
    form_class = AccountLoginForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'account/login.html'
    success_url = reverse_lazy('list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        backend = MongoEngineBackend()
        user = backend.authenticate(
            username=self.request.POST['username'],
            password=self.request.POST['password']
        )
        login(self.request, user.get_user())
        # login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

