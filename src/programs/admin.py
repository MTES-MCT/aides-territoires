from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from programs.models import Program


class ProgramAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('css/admin.css',)}

    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['perimeter']
    fields = [
        'name', 'slug', 'perimeter', 'short_description', 'description', 'aids'
    ]
    autocomplete_fields = ['aids', 'perimeter']


admin.site.register(Program, ProgramAdmin)
