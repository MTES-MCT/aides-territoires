from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from actstream.models import Action, Follow


# The standard actstream's admin are not fancy, so let's not use them.
admin.site.unregister(Action)
admin.site.unregister(Follow)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = (
        'id', 'action_display', 'actor_display', 'verb', 'target_display',
        'target_content_type', 'action_object_display',
        'action_object_content_type', 'timestamp'
    )
    list_filter = ('timestamp', 'verb')
    fieldsets = (
        (None, {
            'fields': ('verb', 'timestamp', 'description')
        }),
        ('Actor', {
            'fields': ('actor', 'actor_content_type', 'actor_object_id'),
        }),
        ('Action', {
            'fields': (
                'action_object', 'action_object_content_type',
                'action_object_object_id'
            ),
        }),
        ('Target', {
            'fields': ('target', 'target_content_type', 'target_object_id'),
        }),
    )
    search_fields = ('verb', 'description', 'actor_object_id')
    readonly_fields = ('actor', 'action_object', 'target')

    def get_admin_url(self, obj):
        """
        Return the admin page URL for the given objet
        """
        content_type = ContentType.objects.get_for_model(obj.__class__)
        app_label = content_type.app_label
        model = content_type.model
        return reverse(f'admin:{app_label}_{model}_change', args=[obj.pk])

    def get_object_display_line(self, obj):
        """
        For the given object, return a display line with HTML link to the admin
        page.
        """
        if not obj:
            return '-'
        url = self.get_admin_url(obj)
        return format_html('<a href="{}">{}</a>', url, obj)

    def action_display(self, obj):
        return self.get_object_display_line(obj)
    action_display.short_description = _('action')

    def actor_display(self, obj):
        return self.get_object_display_line(obj.actor)
    actor_display.short_description = _('actor')

    def target_display(self, obj):
        return self.get_object_display_line(obj.target)
    target_display.short_description = _('target')

    def action_object_display(self, obj):
        return self.get_object_display_line(obj.action_object)
    action_object_display.short_description = _('action object')
