from django.contrib import admin

from alerts.models import Alert


class AlertAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'title', 'date_created', 'date_updated'
    ]


admin.site.register(Alert, AlertAdmin)
