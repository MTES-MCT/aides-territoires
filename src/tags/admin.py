from django.contrib import admin
from django.utils.text import slugify
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'nb_aids']

    def save_model(self, request, obj, form, change):
        """Make sure the tag name is a slug."""
        obj.name = slugify(obj.name, allow_unicode=True)
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(aid_count=Count('aids'))
        return qs

    def nb_aids(self, tag):
        return tag.aid_count
    nb_aids.short_description = _('Number of aids')
    nb_aids.admin_order_field = 'aid_count'


admin.site.register(Tag, TagAdmin)
