from django.contrib import admin

from programs.models import Program


class ProgramAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('css/admin.css',)}

    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fields = [
        'name', 'slug', 'logo', 'short_description', 'description'
    ]
    search_fields = ['name']


admin.site.register(Program, ProgramAdmin)
