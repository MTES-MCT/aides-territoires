from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from stats.models import (AidSearchEvent,
                          AidViewEvent, AidContactClickEvent,
                          AidMatchProjectEvent, AidEligibilityTestEvent,
                          AlertFeedbackEvent, Event)


class ReadOnlyModelAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidContactClickEventAdmin(admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ['id', 'aid', 'source', 'date_created']
    list_filter = ['source']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AidViewEventAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ['id', 'source', 'date_created']
    list_filter = ['source']


class AidSearchEventAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """The model is set to readonly"""
    list_display = ['id', 'source', 'results_count', 'date_created']
    list_filter = ['source']


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


class AidMatchProjectEventAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """The model is set to readonly"""

    list_display = ['id', 'aid', 'project', 'date_created']


class AlertFeedbackEventAdmin(ReadOnlyModelAdminMixin, admin.ModelAdmin):
    """The model is set to readonly"""
    list_display = [
        'alert', 'email', 'rate', 'feedback', 'date_created']
    search_fields = ['alert__email']

    def email(self, obj):
        return obj.alert.email
    email.admin_order_field = 'alert__email'
    email.short_description = _('Email')


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
admin.site.register(AidContactClickEvent, AidContactClickEventAdmin)
admin.site.register(AidSearchEvent, AidSearchEventAdmin)
admin.site.register(AidEligibilityTestEvent, AidEligibilityTestEventAdmin)
admin.site.register(AidMatchProjectEvent, AidMatchProjectEventAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(AlertFeedbackEvent, AlertFeedbackEventAdmin)
