from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


class UserAdmin(BaseUserAdmin):
    """Admin module for users."""

    list_display = ['email', 'full_name', 'date_joined', 'last_login']
    search_fields = ['email', 'full_name']
    ordering = ['full_name', 'email']
    list_filter = ['is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2')}
         ),
    )


admin.site.register(User, UserAdmin)
