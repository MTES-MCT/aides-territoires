from django.contrib import admin

from stats.models import (AidViewEvent, AidSearchEvent,
                          AidMatchProjectEvent, AidEligibilityTestEvent,
                          Event)


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


class AidEligibilityTestEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ['id', 'aid', 'eligibility_test', 'answer_success',
                    'source', 'date_created']
    list_filter = ['eligibility_test', 'source']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidMatchProjectEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ['id', 'aid', 'project', 'date_created']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EventAdmin(admin.ModelAdmin):
    """The model is set to (almost) readonly"""

    list_display = ['category', 'event', 'meta', 'source', 'value',
                    'date_created']
    list_filter = ['category', 'event', 'source']

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AidViewEvent, AidViewEventAdmin)
admin.site.register(AidSearchEvent, AidSearchEventAdmin)
admin.site.register(AidEligibilityTestEvent, AidEligibilityTestEventAdmin)
admin.site.register(AidMatchProjectEvent, AidMatchProjectEventAdmin)
admin.site.register(Event, EventAdmin)
