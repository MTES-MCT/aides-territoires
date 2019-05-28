from django.contrib import admin

from bookmarks.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['owner', 'date_created', 'date_updated']


admin.site.register(Bookmark, BookmarkAdmin)
