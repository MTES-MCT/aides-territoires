from django.contrib import admin

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


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ["recipient"]

    list_display = [
        "message",
        "recipient",
        "date_created",
        "is_read",
    ]
    list_filter = [IsReadFilter]
    search_fields = ["recipient__email", "recipient__last_name", "message"]

    def is_read(self, obj):
        if obj.date_read:
            return True
        else:
            return False

    is_read.boolean = True
    is_read.short_description = "Est lue"
