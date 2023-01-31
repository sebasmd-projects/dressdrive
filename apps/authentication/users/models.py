#
from django.db import models

#
from django.contrib.auth.models import AbstractUser

#
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GlobalUserModel(models.Model):
    first_name = models.CharField(
        _("first name"),
        max_length=150
    )

    last_name = models.CharField(
        _("last name"),
        max_length=150
    )

    created = models.DateTimeField(
        _("created"),
        default=timezone.now
    )

    updated = models.DateTimeField(
        _('updated'),
        auto_now=True
    )

    order = models.PositiveIntegerField(
        'order',
        default=1,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class UserModel(AbstractUser, GlobalUserModel):
    full_name = models.CharField(
        _('full name'),
        max_length=300,
        default=''
    )

    email = models.EmailField(
        _("email address"),
        unique=True
    )
    
    date_joined = ""
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"

        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"{self.id} - {self.full_name}"
    
    class Meta:
        db_table = 'apps_authentication_users'
        verbose_name = 'AUTHENTICATION - User'
        verbose_name_plural = 'AUTHENTICATION - Users'
        ordering = ['order', 'id', 'first_name', 'last_name']