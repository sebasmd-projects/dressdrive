from django.conf import settings
from django.views.generic import edit
from apps.authentication.users import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import resolve_url, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import update_session_auth_hash, logout, views, mixins


class UpdatePasswordView(mixins.LoginRequiredMixin, edit.FormView):
    template_name = "dashboard/user_settings/change_password.html"
    form_class = forms.UpdatePasswordForm
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


class UpdateEmailView(mixins.LoginRequiredMixin, edit.FormView):
    template_name = "dashboard/user_settings/change_email.html"
    form_class = forms.UpdateEmailForm

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


class UpdateProfileView(mixins.LoginRequiredMixin, edit.FormView):
    template_name = "dashboard/user_settings/profile.html"
    form_class = forms.GeneralUpdateProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user

        context["profile_avatar"] = forms.UpdateProfileAvatarForm(
            user=current_user
        )

        context["profile"] = forms.UpdateProfileForm(user=current_user, initial={
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


class UpdateNotificationsView(mixins.LoginRequiredMixin, edit.FormView):
    template_name = "dashboard/user_settings/notifications.html"
    form_class = forms.UpdateNotificationsForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('settings_user:user_change_notifications')


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above

UserModel = get_user_model()


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class PasswordResetView(views.PasswordResetView):
    template_name = "authentication/password_reset/password_reset_form.html"
    
    email_template_name = "authentication/password_reset/password_reset_email.html"
    subject_template_name = "authentication/password_reset/password_reset_subject.txt"
    
    success_url = reverse_lazy("settings_user:password_reset_done")
    form_class = forms.PasswordResetForm
    from_email = settings.DEFAULT_FROM_EMAIL
    title = _("Password reset")
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('settings_user:user_change_password')
        return super().dispatch(request, *args, **kwargs)


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = "authentication/password_reset/password_reset_done.html"


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    success_url = reverse_lazy("settings_user:password_reset_complete")
    template_name = "authentication/password_reset/password_reset_confirm.html"
    title = _("Enter new password")


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = "authentication/password_reset/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context
