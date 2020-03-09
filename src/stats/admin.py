from django.contrib import admin

from stats.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'date_created']


admin.site.register(Event, EventAdmin)
