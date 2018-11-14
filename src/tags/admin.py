from django.contrib import admin
from django.utils.text import slugify

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

    def save_model(self, request, obj, form, change):
        """Make sure the tag name is a slug."""
        obj.name = slugify(obj.name)
        return super().save_model(request, obj, form, change)


admin.site.register(Tag, TagAdmin)
