from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from core.forms import RichTextField
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from blog.models import BlogPost, BlogPostCategory, PromotionPost
from categories.fields import CategoryMultipleChoiceField


class BlogPostForm(forms.ModelForm):
    text = RichTextField(label="Contenu", required=False)

    class Meta:
        model = BlogPost
        fields = "__all__"


class BlogPostAdmin(admin.ModelAdmin):

    list_display = ["title", "category", "status", "date_created"]
    search_fields = ["title"]
    list_filter = ["status", "category"]
    autocomplete_fields = ["author"]

    form = BlogPostForm
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["date_created", "date_updated", "date_published"]

    fieldsets = [
        (
            "",
            {
                "fields": (
                    "title",
                    "slug",
                    "author",
                    "short_text",
                    "text",
                    "logo",
                    "category",
                )
            },
        ),
        ("Administration", {"fields": ("status",)}),
        (
            "SEO",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                )
            },
        ),
        (
            "Données diverses",
            {
                "fields": (
                    "date_created",
                    "date_updated",
                    "date_published",
                )
            },
        ),
    ]

    class Media:
        css = {
            "all": (
                "/static/css/admin.css",
                "/static/trumbowyg/dist/ui/trumbowyg.css",
            )
        }
        js = [
            "admin/js/jquery.init.js",
            "/static/js/shared_config.js",
            "/static/js/plugins/softmaxlength.js",
            "/static/js/search/enable_softmaxlength.js",
            "/static/trumbowyg/dist/trumbowyg.js",
            "/static/trumbowyg/dist/langs/fr.js",
            "/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js",
            "/static/jquery-resizable-dom/dist/jquery-resizable.js",
            "/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js",
            "/static/js/enable_rich_text_editor.js",
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


class BlogPostCategoryAdmin(admin.ModelAdmin):

    list_display = ["name"]
    fields = ["name", "slug", "description", "date_created"]
    search_fields = ["name"]
    ordering = ["name"]

    prepopulated_fields = {"slug": ("name",)}


class PromotionPostForm(forms.ModelForm):

    categories = CategoryMultipleChoiceField(
        label="Sous-thématiques",
        required=False,
        widget=FilteredSelectMultiple("Sous-thématiques", True),
    )

    class Meta:
        model = PromotionPost
        fields = "__all__"


class PromotionPostAdmin(admin.ModelAdmin):

    list_display = ["title", "status", "date_created"]
    search_fields = ["title"]
    ordering = ["title"]
    search_fields = ["id", "title"]
    list_filter = ["status", "date_created"]

    form = PromotionPostForm
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ["backers", "programs", "perimeter"]
    readonly_fields = ["date_created", "date_updated"]

    fieldsets = [
        (
            "Présentation",
            {
                "fields": (
                    "title",
                    "slug",
                    "short_text",
                    "button_title",
                    "button_link",
                )
            },
        ),
        (
            "Filtres conditionnant l'affichage",
            {
                "fields": (
                    "backers",
                    "programs",
                    "perimeter",
                    "categories",
                )
            },
        ),
        ("Administration", {"fields": ("status",)}),
        (
            "Données diverses",
            {
                "fields": (
                    "date_created",
                    "date_updated",
                )
            },
        ),
    ]


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogPostCategory, BlogPostCategoryAdmin)
admin.site.register(PromotionPost, PromotionPostAdmin)
