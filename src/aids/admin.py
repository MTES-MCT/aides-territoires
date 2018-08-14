from django.contrib import admin

from aids.models import Aid


class AidAdmin(admin.ModelAdmin):
    pass


admin.site.register(Aid, AidAdmin)
