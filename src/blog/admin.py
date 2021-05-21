from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

from core.forms import RichTextField
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS
from admin_auto_filters.filters import AutocompleteFilter

from blog.models import BlogPost, BlogPostCategory, PromotionPost
from categories.fields import CategoryMultipleChoiceField
from categories.models import Category


class BlogPostForm(forms.ModelForm):
    text = RichTextField(label=_('Text'), required=False)

    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogPostAdmin(admin.ModelAdmin):

    form = BlogPostForm
    list_display = ['title', 'category', 'date_created', 'status']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    list_filter = ['status', 'category']

    fieldsets = [
        (_('General content'), {
            'fields': (
                'title',
                'slug',
                'short_text',
                'logo',
                'text',
                'category',
                'status',
                'date_created',
                'date_published',
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
            )
        }),
    ]

    class Media:
        css = {
            'all': (
                '/static/css/admin.css',
                '/static/trumbowyg/dist/ui/trumbowyg.css',
            )
        }
        js = [
            'admin/js/jquery.init.js',
            '/static/js/shared_config.js',
            '/static/js/plugins/softmaxlength.js',
            '/static/js/search/enable_softmaxlength.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js',
            '/static/trumbowyg/dist/plugins/resizimg/resizable-resolveconflict.js',  # noqa
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ] + TRUMBOWYG_UPLOAD_ADMIN_JS


class BlogPostCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    fields = ['name', 'slug', 'description', 'date_created']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']


class PromotionPostForm(forms.ModelForm):

    categories = CategoryMultipleChoiceField(
        label=_('Categories'),
        required=False,
        widget=FilteredSelectMultiple(_('Categories'), True))

    class Meta:
        model = PromotionPost
        fields = '__all__'


class PromotionPostAdmin(admin.ModelAdmin):
    form = PromotionPostForm
    list_display = ['title', 'status', 'date_created']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    ordering = ['title']
    autocomplete_fields = ['backers', 'programs', 'perimeter']
    search_fields = ['id', 'title']
    list_filter = ['status', 'date_created',]

    fieldsets = [
        (_('Promotion post presentation'), {
            'fields': (
                'title',
                'slug',
                'short_text',
                'button_title',
                'button_link',
            )
        }),

        (_('Promotion post filter for display'), {
            'fields': (
                'backers',
                'programs',
                'perimeter',
                'categories',
            )
        }),

        (_('Promotion post admin'), {
            'fields': (
                'status',
            )
        }),

        (_('Misc data'), {
            'fields': (
                'date_created',
            )
        }),
    ]

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogPostCategory, BlogPostCategoryAdmin)
admin.site.register(PromotionPost, PromotionPostAdmin)
