from django.contrib import admin
from django.utils import timezone

from core.constants import YES_NO_CHOICES
from notifications import models


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


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
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
