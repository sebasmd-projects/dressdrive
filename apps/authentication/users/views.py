import unicodedata
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import redirect
from apps.authentication.users import forms
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.views.generic import edit, TemplateView
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import get_user_model, logout, update_session_auth_hash, logout, mixins

UserModel = get_user_model()


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )


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


class PasswordResetEmailView(edit.FormView):
    template_name = "authentication/password_reset/password_reset_email_form.html"
    success_url = reverse_lazy("settings_user:user_password_email_sended")
    form_class = forms.PasswordResetEmailForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('settings_user:user_change_password')
        return super().dispatch(request, *args, **kwargs)

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def form_valid(self, form):
        email = form.cleaned_data['email']
        email_field_name = UserModel.get_email_field_name()

        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            context = {
                "email": user_email,
                "uid": uid,
                "user": user.full_name(),
                "token": token,
                "url": f"{settings.BASE_URL}{reverse('settings_user:password_reset_form', kwargs={'uidb64':uid, 'token':token})}"
            }
            subject = f"[{settings.BASE_URL}] - Reset Password"
            from_email = "no-reply@sebasmd.com"
            to_email = [email]
            text_content = render_to_string(
                "authentication/password_reset/email/password_reset_email_content.txt", context)
            html_content = render_to_string(
                "authentication/password_reset/email/password_reset_email_content.html", context)
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return super(PasswordResetEmailView, self).form_valid(form)


class PasswordResetEmailSentView(TemplateView):
    template_name = "authentication/password_reset/password_reset_email_sent.html"


class PasswordResetFormView(edit.FormView):
    template_name = "authentication/password_reset/password_reset_form.html"
    token_generator = default_token_generator
    form_class = forms.PasswordResetFormForm
    success_url = reverse_lazy('authentication_login:user-login')

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def form_valid(self, form):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        user = self.get_user(uidb64)
        if user is not None and self.token_generator.check_token(user, token):
            user.set_password(form.cleaned_data['confirm_password'])
            user.save()
        return super(PasswordResetFormView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        user = self.get_user(uidb64)
        if (user is None) or (self.token_generator.check_token(user, token) is False):
            return redirect('settings_user:user_password_email_form')
        return super().dispatch(request, *args, **kwargs)