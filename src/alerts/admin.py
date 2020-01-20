from django.contrib import admin

from alerts.models import Alert


class AlertAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'title', 'latest_alert_date', 'date_created', 'validated',
        'date_validated'
    ]
    list_filter = ['validated']


admin.site.register(Alert, AlertAdmin)
