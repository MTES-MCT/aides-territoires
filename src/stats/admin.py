from django.contrib import admin

from stats.models import AidViewEvent, Event


class AidViewEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""
    list_display = ['id', 'aid', 'source', 'date_created']
    list_filter = ['source']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EventAdmin(admin.ModelAdmin):
    list_display = ['category', 'event', 'meta', 'source', 'value',
                    'date_created']


admin.site.register(AidViewEvent, AidViewEventAdmin)
admin.site.register(Event, EventAdmin)
