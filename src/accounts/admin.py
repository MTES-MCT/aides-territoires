from django import forms
from django.db.models import Count, Q, CharField, Value as V
from django.db.models.functions import Concat
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.admin import InputFilter
from aids.models import Aid
from accounts.models import User


class AuthorFilter(InputFilter):
    parameter_name = 'author'
    title = _('Author')

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            qs = queryset \
                .annotate(
                    author_name=Concat(
                        'author__first_name', V(' '), 'author__last_name',
                        output_field=CharField())) \
                .filter(Q(author_name__icontains=value))
            return qs


class SearchPageAdministratorFilter(admin.SimpleListFilter):
    """Custom admin filter to target users who are
    search page administrators."""

    title = 'Administrateur de PP ?'
    parameter_name = 'is_administrator_of_search_pages'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.is_administrator_of_search_pages()
        elif value == 'No':
            return queryset.filter(administrator_of_search_pages__isnull=True)
        return queryset


class ApiTokenFilter(admin.SimpleListFilter):
    """Custom admin filter to target users with API Tokens."""

    title = 'Token API ?'
    parameter_name = 'has_api_token'

    def lookups(self, request, model_admin):
        return (
            ('Yes', _('Yes')),
            ('No', _('No')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.with_api_token()
        elif value == 'No':
            return queryset.filter(auth_token__isnull=True)
        return queryset


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
        'email', 'first_name', 'last_name', 'organization',
        'is_contributor', 'nb_aids',
        'is_certified', 'in_mailing_list', 'date_joined', 'last_login'
    ]
    list_editable = ['first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['last_name', 'email']

    list_filter = ['is_superuser', 'is_contributor',
                   SearchPageAdministratorFilter, ApiTokenFilter,
                   'is_certified', 'ml_consent']

    readonly_fields = ['nb_aids', 'api_token', 'last_login', 'date_joined']

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
                'is_certified'
            )
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
            )
        }),
        (_('Professional info'), {
            'fields': (
                'organization',
                'role',
                'contact_phone'
            )
        }),
        (_('Contributor space'), {
            'fields': (
                'is_contributor',
                'nb_aids',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_superuser',
                'api_token'
            )
        }),
        (_('Misc.'), {
            'fields': (
                'ml_consent',
                'last_login',
                'date_joined',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_contributor',
                'is_certified',
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

    def in_mailing_list(self, user):
        return user.ml_consent
    in_mailing_list.short_description = mark_safe(
        _('<abbr title="Newsletter subscriber">NL</abbr>'))
    in_mailing_list.boolean = True

    def api_token(self, user):
        try:
            token = user.auth_token
            return token.key
        except AttributeError:
            return format_html(
                'Non. <a href="{obj_url}">Créer</a>',
                obj_url=reverse('admin:authtoken_tokenproxy_changelist'))
    api_token.short_description = "Token API"

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
