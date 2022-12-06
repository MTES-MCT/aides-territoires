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
    list_filter = [("recipient", admin.RelatedOnlyFieldListFilter), IsReadFilter]
    search_fields = ["recipient, message"]
