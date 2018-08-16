from django.contrib import admin

from backers.models import Backer


class BackerAdmin(admin.ModelAdmin):
    """Admin module for aid backers."""

    list_display = ['name']
    search_fields = ['name']


admin.site.register(Backer, BackerAdmin)
