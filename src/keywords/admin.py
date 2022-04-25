from django.contrib import admin

from keywords.models import Keyword


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    ordering = ["name"]


admin.site.register(Keyword, KeywordAdmin)
