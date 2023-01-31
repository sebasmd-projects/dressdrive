from django.contrib.auth.backends import BaseBackend
from apps.authentication.users.models import UserModel


class EmailOrUsernameModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = UserModel.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        
    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None