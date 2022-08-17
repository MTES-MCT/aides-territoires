from django.contrib import admin

from keywords.models import Keyword, SynonymList


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    ordering = ["name"]


class SynonymListAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "slug", "keywords"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    readonly_fields = ["date_created"]
    autocomplete_fields = ["keywords"]
    ordering = ["name"]


admin.site.register(Keyword, KeywordAdmin)
admin.site.register(SynonymList, SynonymListAdmin)
