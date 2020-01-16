from django.contrib import admin

from alerts.models import Bookmark


class BookmarkAdmin(admin.ModelAdmin):
    list_display = [
        'owner', 'title', 'send_email_alert', 'date_created', 'date_updated'
    ]


admin.site.register(Bookmark, BookmarkAdmin)
