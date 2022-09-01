from django.contrib import admin
from django import forms
from django.utils.html import format_html

from keywords.models import Keyword, SynonymList


class KeywordAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    ordering = ["name"]


class SynonymListAdminForm(forms.ModelForm):
    """Custom form for inline synonymList edition."""

    keywords_list = forms.CharField(
        label="Liste de mots clés", required=False, max_length=1800
    )


class SynonymListAdmin(admin.ModelAdmin):
    list_display = ["name", "keywords_list"]
    list_editable = ["keywords_list"]
    fields = ["name", "slug", "keywords_list", "current_keywords_list"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
    readonly_fields = ["date_created", "current_keywords_list"]
    ordering = ["name"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(SynonymListAdmin, self).formfield_for_dbfield(
            db_field, **kwargs
        )
        if db_field.name == "keywords_list":
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    @admin.display()
    def current_keywords_list(self, obj):
        keywords_list_array = obj.keywords_list.split(",")
        keywords_list_html = format_html("<p>")
        for keyword in keywords_list_array:
            keywords_list_html += format_html(f"{keyword} <br/>")
        keywords_list_html += format_html("</p>")
        return keywords_list_html

    current_keywords_list.short_description = "Liste de mots clés (avant modification)"
    current_keywords_list.allow_tags = True


admin.site.register(Keyword, KeywordAdmin)
admin.site.register(SynonymList, SynonymListAdmin)
