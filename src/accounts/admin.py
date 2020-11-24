from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


class UserAdmin(BaseUserAdmin):
    """Admin module for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'is_certified', 'ml_consent',
        'date_joined', 'last_login'
    ]
    list_editable = ['first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['last_name', 'email']
    list_filter = ['is_superuser', 'is_certified', 'ml_consent']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_certified')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2',
                'is_certified'
            )}
         ),
    )


admin.site.register(User, UserAdmin)
