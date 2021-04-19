from django.contrib import admin

from stats.models import (AidViewEvent, AidSearchEvent, Event,
                          AidMatchProjectEvent)


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


class AidSearchEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""
    list_display = ['id', 'source', 'results_count', 'date_created']
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


class AidMatchProjectEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""
    list_display = ['id', 'aid', 'project', 'date_created']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AidViewEvent, AidViewEventAdmin)
admin.site.register(AidSearchEvent, AidSearchEventAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(AidMatchProjectEvent, AidMatchProjectEventAdmin)
