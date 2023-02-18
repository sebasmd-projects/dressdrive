from datetime import timedelta, date
#
from django.db import models
from django.db.models.signals import post_save

#
from django.contrib.auth.models import AbstractUser

#
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

#
from apps.authentication.users.managers import UserManager
from apps.authentication.users.signals import avatar_directory_path, optimize_image
#


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
        _("updated"),
        auto_now=True
    )

    order = models.PositiveIntegerField(
        _("order"),
        default=1,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class UserModel(AbstractUser, GlobalUserModel):
    avatar = models.ImageField(
        _("profile picture"),
        upload_to=avatar_directory_path,
        blank=True,
        null=True
    )

    phone = models.CharField(
        _("phone"),
        max_length=20,
        default=0
    )

    gender = models.CharField(
        _("gender"),
        max_length=30,
        default="Other"
    )

    birthday = models.DateField(
        _("Birthday"),
        default=(timezone.now)
    )

    email = models.EmailField(
        _("email address"),
        unique=True
    )

    privacy = models.BooleanField(
        _("Terms and Conditions"),
        default=False
    )

    date_joined = ""

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "apps_authentication_users"
        verbose_name = "AUTHENTICATION - User"
        verbose_name_plural = "AUTHENTICATION - Users"
        ordering = ["order", "id", "first_name", "last_name"]

    def save(self, *args, **kwargs):
        self.first_name = f"{self.first_name}".title()
        self.last_name = f"{self.last_name}".title()
        self.username = f"{self.username.lower()}"
        super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.id} - {self.first_name} {self.last_name}"

    def age(self):
        return date.today().year - self.birthday.year - (
            (
                date.today().month, date.today().day
            ) < (
                self.birthday.month, self.birthday.day
            )
        )


post_save.connect(optimize_image, sender=UserModel)
