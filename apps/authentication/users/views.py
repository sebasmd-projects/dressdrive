from django.urls import reverse_lazy, reverse
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from apps.authentication.users.forms import UpdateEmailForm, UpdatePasswordForm, UpdateProfileForm, UpdateNotificationsForm


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


class UpdateEmailView(LoginRequiredMixin, FormView):
    template_name = "dashboard/user_settings/change_email.html"
    form_class = UpdateEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['new_email']
        user.save()
        return super(UpdateEmailView, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('settings_user:user_change_email')

class UpdateProfileView(LoginRequiredMixin, FormView):
    template_name = "dashboard/user_settings/profile.html"
    form_class = UpdateProfileForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('settings_user:user_change_profile')
        
class UpdateNotificationsView(LoginRequiredMixin, FormView):
    template_name = "dashboard/user_settings/notifications.html"
    form_class = UpdateNotificationsForm
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('settings_user:user_change_notifications')