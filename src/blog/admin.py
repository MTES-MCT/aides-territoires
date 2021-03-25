from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.forms import RichTextField
from upload.settings import TRUMBOWYG_UPLOAD_ADMIN_JS

from blog.models import Post


class PostForm(forms.ModelForm):
    text = RichTextField(label=_('Text'), required=False)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):

    form = PostForm
    list_display = ['title', 'categorie', 'date_created', 'status']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    list_filter = ['title', 'status', 'categorie', ]

    fieldsets = [
        (_('General content'), {
            'fields': (
                'title',
                'slug',
                'short_text',
                'text',
                'categorie',
                'status',
                'date_created',
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


admin.site.register(Post, PostAdmin)
