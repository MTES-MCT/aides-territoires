from django import forms
from django.db.models import Count
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from aids.models import Aid
from accounts.models import User


class UserAdminForm(forms.ModelForm):
    """Custom form for inline user edition."""

    first_name = forms.CharField(
        label=_('First name'),
        required=False,
        max_length=256)
    last_name = forms.CharField(
        label=_('Last name'),
        required=False,
        max_length=256)


class UserAdmin(BaseUserAdmin):
    """Admin module for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'organization', 'nb_aids',
        'is_certified', 'in_mailing_list', 'date_joined', 'last_login'
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(aid_count=Count('aids'))
        return qs

    def nb_aids(self, user):
        return user.aid_count
    nb_aids.short_description = "Nombre d'aides"
    nb_aids.admin_order_field = 'aid_count'

    def in_mailing_list(self, obj):
        return obj.ml_consent
    in_mailing_list.short_description = mark_safe(
        _('<abbr title="Newsletter subscriber">NL</abbr>'))
    in_mailing_list.boolean = True

    def get_changelist_form(self, request, **kwargs):
        return UserAdminForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add aids by same author in context."""

        other_aids = Aid.objects \
            .existing() \
            .filter(author_id=object_id) \
            .prefetch_related('financers') \
            .order_by('-date_published')

        context = extra_context or {}
        context['other_aids'] = other_aids

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=context)


admin.site.register(User, UserAdmin)
