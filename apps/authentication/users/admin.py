from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.authentication.users.models import UserModel


@admin.register(UserModel)
class UserModelAdmin(UserAdmin):
    list_display = (
        'id',
        'full_name',
        'email',
        'username',
        'is_staff',
        'is_superuser',
        'created',
        'updated'
    )

    list_display_links = (
        'id',
        'full_name',
        'email',
        'username'
    )

    fieldsets = (
        (
            _('User'),
            {
                'fields': (
                    'username',
                    'email',
                    'phone',
                    'password'
                )
            }
        ),
        (
            _('User Information'),
            {
                'fields': (
                    'avatar',
                    'full_name',
                    'first_name',
                    'last_name',
                    'gender',
                    'birthday',
                    'age'
                )
            }
        ),
        (
            _('Location'),
            {
                'fields': (
                    'latitude',
                    'longitude',
                    'location'
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'privacy'
                ),
            },
        ),
        (
            _('Dates'),
            {
                'fields': (
                    'last_login',
                    'created',
                    'updated',
                )
            }
        ),
        (
            None,
            {
                'fields': (
                    'order',
                )
            }
        )
    )

    ordering = (
        'id',
        'email',
        'first_name',
        'last_name'
    )

    readonly_fields = (
        'full_name',
        'last_login',
        'date_joined',
        'created',
        'updated',
        'age'
    )

    def full_name(self, obj):
        return obj.full_name()
    
    def age(self, obj):
        return obj.age()
    
    age.short_description = _('Full Name')
    age.short_description = _('Age')