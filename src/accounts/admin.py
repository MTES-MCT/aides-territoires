from django import forms
from django.db.models import Count, Q, CharField, Value as V
from django.db.models.functions import Concat
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from core.admin import InputFilter
from core.constants import YES_NO_CHOICES
from accounts.resources import UserResource
from aids.models import Aid
from accounts.models import User, UserLastConnexion
from exporting.tasks import export_users_as_csv, export_users_as_xlsx
from exporting.utils import get_admin_export_message


class AuthorFilter(InputFilter):
    parameter_name = "author"
    title = "Auteur"

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            qs = queryset.annotate(
                author_name=Concat(
                    "author__first_name",
                    V(" "),
                    "author__last_name",
                    output_field=CharField(),
                )
            ).filter(Q(author_name__icontains=value))
            return qs


class SearchPageAdministratorFilter(admin.SimpleListFilter):
    """Custom admin filter to target users who are
    search page administrators."""

    title = "Administrateur de PP ?"
    parameter_name = "is_administrator_of_search_pages"

    def lookups(self, request, model_admin):
        return YES_NO_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.search_page_admins()
        elif value == "No":
            return queryset.filter(search_pages__isnull=True)
        return queryset


class AnimatorFilter(admin.SimpleListFilter):
    """Custom admin filter to target users who are animators."""

    title = "Animateur ?"
    parameter_name = "is_animator"

    def lookups(self, request, model_admin):
        return YES_NO_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.animators()
        elif value == "No":
            return queryset.filter(animator_perimeter__isnull=True)
        return queryset


class ApiTokenFilter(admin.SimpleListFilter):
    """Custom admin filter to target users with API Tokens."""

    title = "Token API ?"
    parameter_name = "has_api_token"

    def lookups(self, request, model_admin):
        return YES_NO_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.with_api_token()
        elif value == "No":
            return queryset.filter(auth_token__isnull=True)
        return queryset


class UserAdminForm(forms.ModelForm):
    """Custom form for inline user edition."""

    first_name = forms.CharField(label="Prénom", required=False, max_length=256)
    last_name = forms.CharField(label="Nom", required=False, max_length=256)


class UserAdmin(BaseUserAdmin, ImportExportActionModelAdmin):
    """Admin module for users."""

    resource_class = UserResource
    actions = ["export_csv", "export_xlsx"]
    formats = [base_formats.CSV, base_formats.XLSX]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "contributor_organization",
        "is_contributor",
        "nb_aids",
        "is_certified",
        "in_mailing_list",
        "date_created",
        "last_login",
    ]
    list_editable = ["first_name", "last_name"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["last_name", "email"]

    list_filter = [
        "is_superuser",
        "is_contributor",
        "is_beneficiary",
        SearchPageAdministratorFilter,
        AnimatorFilter,
        ApiTokenFilter,
        "is_certified",
        "ml_consent",
        "groups",
    ]

    autocomplete_fields = [
        "animator_perimeter",
        "beneficiary_organization",
        "proposed_organization",
        "invitation_author",
    ]
    readonly_fields = [
        "nb_aids",
        "administrator_of_search_pages_list",
        "api_token",
        "last_login",
        "date_created",
        "date_updated",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "is_certified",
                )
            },
        ),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "image")}),
        (
            "Espace contributeur",
            {
                "fields": (
                    "is_contributor",
                    "contributor_organization",
                    "contributor_role",
                    "contributor_contact_phone",
                    "nb_aids",
                )
            },
        ),
        (
            "Espace bénéficiaire",
            {
                "fields": (
                    "is_beneficiary",
                    "beneficiary_function",
                    "beneficiary_role",
                    "beneficiary_organization",
                )
            },
        ),
        (
            "Fusion d'organisation",
            {
                "fields": (
                    "proposed_organization",
                    "invitation_author",
                    "invitation_date",
                    "join_organization_date",
                )
            },
        ),
        (
            "Espace administrateur",
            {
                "fields": (
                    "administrator_of_search_pages_list",
                    "groups",
                )
            },
        ),
        ("Espace animateur", {"fields": ("animator_perimeter",)}),
        ("Permissions", {"fields": ("is_superuser", "api_token")}),
        (
            "Préférences de notifications",
            {"fields": ("notification_email_frequency",)},
        ),
        (
            "Données diverses",
            {
                "fields": (
                    "ml_consent",
                    "acquisition_channel",
                    "acquisition_channel_comment",
                    "last_login",
                    "date_created",
                    "date_updated",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_contributor",
                    "is_certified",
                ),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(aid_count=Count("aids"))
        # TODO: if not superuser, only return user's colleagues
        return qs

    def nb_aids(self, user):
        return user.aid_count

    nb_aids.short_description = "Nombre d'aides"
    nb_aids.admin_order_field = "aid_count"

    def administrator_of_search_pages_list(self, user):
        search_pages = user.search_pages.all()
        if not search_pages:
            return "Aucune"
        else:
            html = ""
            for search_page in search_pages:
                html += format_html(
                    '<a href="{obj_url}">{obj_name}</a><br />',
                    obj_url=reverse(
                        "admin:search_searchpage_change", args=[search_page.id]
                    ),
                    obj_name=search_page,
                )
            return format_html(html)

    administrator_of_search_pages_list.short_description = "Recherche personnalisée"

    def in_mailing_list(self, user):
        return user.ml_consent

    in_mailing_list.short_description = mark_safe(  # nosec B308
        '<abbr title="Dans la newsletter">NL</abbr>'
    )
    in_mailing_list.boolean = True

    def api_token(self, user):
        try:
            token = user.auth_token
            return token.key
        except AttributeError:
            return format_html(
                'Non. <a href="{obj_url}">Créer</a>',
                obj_url=reverse("admin:authtoken_tokenproxy_changelist"),
            )

    api_token.short_description = "Token API"

    def get_changelist_form(self, request, **kwargs):
        return UserAdminForm

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """Add aids by same author in context."""

        other_aids = (
            Aid.objects.existing()
            .filter(author_id=object_id)
            .prefetch_related("financers")
            .order_by("-date_published")
        )

        context = extra_context or {}
        context["other_aids"] = other_aids

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=context
        )

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        users_id_list = list(queryset.values_list("id", flat=True))
        export_users_as_csv.delay(users_id_list, request.user.id)
        self.show_export_message(request)

    export_csv.short_description = (
        "Exporter les utilisateurs sélectionnés en CSV en tâche de fond"
    )

    def export_xlsx(self, request, queryset):
        users_id_list = list(queryset.values_list("id", flat=True))
        export_users_as_xlsx.delay(users_id_list, request.user.id)
        self.show_export_message(request)

    export_xlsx.short_description = (
        "Exporter les utilisateurs sélectionnés en XLSX en tâche de fond"
    )


class UserLastConnexionAdmin(admin.ModelAdmin):
    """Admin module for users last connexions."""

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    list_display = ["user", "last_connexion_with_seconds"]
    search_fields = ["user__email"]
    ordering = ["user", "last_connexion"]

    list_filter = ["last_connexion"]

    readonly_fields = ["user", "last_connexion_with_seconds"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "last_connexion_with_seconds",
                )
            },
        ),
    )

    def last_connexion_with_seconds(self, obj):
        return obj.last_connexion.strftime("%d %b %Y %H:%M:%S")

    last_connexion_with_seconds.short_description = "Dernière connexion"
    last_connexion_with_seconds.admin_order_field = "last_connexion"


admin.site.register(User, UserAdmin)
admin.site.register(UserLastConnexion, UserLastConnexionAdmin)
