from django.contrib import admin

from programs.models import Program


class ProgramAidInline(admin.TabularInline):
    model = Program.aids.through
    autocomplete_fields = ['aid']
    extra = 16


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['perimeter']
    fields = ['name', 'slug', 'perimeter', 'short_description', 'description']
    inlines = [ProgramAidInline]


admin.site.register(Program, ProgramAdmin)
