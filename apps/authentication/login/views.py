from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.authentication.login.forms import UserLoginForm, UpdatePasswordForm


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


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = "dashboard/user_settings/change_password.html"
    form_class = UpdatePasswordForm
    login_url = reverse_lazy('authentication_login:user-login')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password'])
        user.save()
        update_session_auth_hash(self.request, user)
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('admin:index')
    
    # def form_invalid(self, form):
    #     user = self.request.user
    #     user.set_password('juan1999@')
    #     user.save()
    #     return super(UpdatePasswordView, self).form_invalid(form)