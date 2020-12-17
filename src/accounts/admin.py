from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


class UserAdmin(BaseUserAdmin):
    """Admin module for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'organization', 'is_certified',
        'in_mailing_list', 'date_joined', 'last_login'
    ]
    list_editable = ['first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['last_name', 'email']
    list_filter = ['is_superuser', 'is_certified', 'ml_consent']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_certified')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Professional info'), {'fields': (
            'organization', 'role', 'contact_phone')}),
        (_('Permissions'), {'fields': ('is_superuser',)}),
        (_('Misc.'), {'fields': (
            'ml_consent', 'last_login', 'date_joined',)}),
    )
    readonly_fields = ('last_login', 'date_joined')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2',
                'is_certified'
            )}
         ),
    )

    def in_mailing_list(self, obj):
        return obj.ml_consent
    in_mailing_list.short_description = mark_safe(
        _('<abbr title="Newsletter subscriber">NL</abbr>'))
    in_mailing_list.boolean = True


admin.site.register(User, UserAdmin)
