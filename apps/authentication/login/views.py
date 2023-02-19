from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from apps.authentication.login.forms import UserLoginForm


class UserLoginView(FormView):
    template_name = "authentication/login.html"
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('admin:index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data['remember_me']

        user = authenticate(username=username, password=password)

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        login(self.request, user)

        return super(UserLoginView, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('admin:index')


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                'authentication_login:user-login'
            )
        )

