#
from django.urls import reverse

#
from django.views.generic.edit import (
    FormView,
)

#
from apps.authentication.register.forms import UserRegisterForm
from apps.authentication.users.models import UserModel


class UserRegisterView(FormView):
    template_name = "authentication/register.html"
    form_class = UserRegisterForm

    def form_valid(self, form):
        UserModel.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password'],
            privacy=form.cleaned_data['privacy']
        )
        return super(UserRegisterView, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('authentication_login:user-login')
