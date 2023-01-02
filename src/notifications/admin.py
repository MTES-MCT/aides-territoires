from django.contrib import admin
from django.forms import ModelForm
from django.utils import timezone

from core.constants import YES_NO_CHOICES
from core.forms import RichTextField
from notifications import models

from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS


class IsReadFilter(admin.SimpleListFilter):
    """Custom admin filter to target users with API Tokens."""

    title = "Est lue"
    parameter_name = "is_read"

    def lookups(self, request, model_admin):
        return YES_NO_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.filter(date_read__isnull=False)
        elif value == "No":
            return queryset.filter(date_read__isnull=True)
        return queryset


@admin.action(description="Marquer les notifications sélectionnées comme lues")
def mark_read(modeladmin, request, queryset):
    queryset.update(date_read=timezone.now())


@admin.action(description="Marquer les notifications sélectionnées comme non lues")
def mark_unread(modeladmin, request, queryset):
    queryset.update(date_read=None)


class NotificationAdminForm(ModelForm):
    message = RichTextField(label="message")


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm

    actions = [mark_read, mark_unread]

    autocomplete_fields = ["recipient"]

    list_display = [
        "truncated_title",
        "notification_type",
        "recipient",
        "date_created",
        "is_read",
    ]
    list_filter = ["notification_type", IsReadFilter]
    search_fields = ["recipient__email", "recipient__last_name", "message"]

    readonly_fields = ["date_created", "id"]

    def is_read(self, obj):
        if obj.date_read:
            return True
        else:
            return False

    is_read.boolean = True
    is_read.short_description = "Est lue"

    def truncated_title(self, obj):
        return obj.truncate_title()

    truncated_title.short_description = "titre"

    class Media:
        css = {
            "all": (
                "/static/css/admin.css",
                "/static/trumbowyg/dist/ui/trumbowyg.css",
            )
        }
        js = [
            "admin/js/jquery.init.js",
            "/static/js/shared_config.js",
            "/static/trumbowyg/dist/trumbowyg.js",
            "/static/trumbowyg/dist/langs/fr.js",
            "/static/js/enable_rich_text_editor.js",
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS
