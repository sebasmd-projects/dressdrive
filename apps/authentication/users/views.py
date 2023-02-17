from django.urls import reverse_lazy, reverse
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.edit import FormView

from apps.authentication.users.forms import (
    UpdateEmailForm,
    UpdatePasswordForm,
    UpdateProfileAvatarForm,
    UpdateProfileForm,
    GeneralUpdateProfileForm,
    UpdateNotificationsForm
)
from apps.authentication.users.models import UserModel


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
    form_class = GeneralUpdateProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user

        context["profile_avatar"] = UpdateProfileAvatarForm(
            user=current_user
        )

        context["profile"] = UpdateProfileForm(user=current_user, initial={
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone': current_user.phone,
            'gender': current_user.gender
        })
        return context

    def form_valid(self, form):
        user = self.request.user

        if form.cleaned_data['avatar']:
            user.avatar = form.cleaned_data['avatar']

        if form.cleaned_data['first_name']:
            user.first_name = form.cleaned_data['first_name']

        if form.cleaned_data['last_name']:
            user.last_name = form.cleaned_data['last_name']

        if form.cleaned_data['phone']:
            user.phone = form.cleaned_data['phone']

        if form.cleaned_data['gender']:
            user.gender = form.cleaned_data['gender']

        user.save()
        return super(UpdateProfileView, self).form_valid(form)

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


