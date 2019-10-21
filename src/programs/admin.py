from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from programs.models import Program


class AidMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        label_elements = [
            obj.name, obj.perimeter.name if obj.perimeter else '',
            ', '.join(b.name for b in obj.backers.all())
        ]
        return ' / '.join(filter(None, label_elements))


published_aids_qs = Aid.objects \
    .published() \
    .select_related('perimeter') \
    .prefetch_related('backers')


class ProgramForm(forms.ModelForm):
    aids = AidMultipleChoiceField(
        queryset=published_aids_qs,
        widget=admin.widgets.FilteredSelectMultiple(
            _('Aids'),
            is_stacked=True,
        ))


class ProgramAdmin(admin.ModelAdmin):

    class Media:
        css = {'all': ('css/admin.css',)}

    form = ProgramForm
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['perimeter']
    fields = [
        'name', 'slug', 'perimeter', 'short_description', 'description', 'aids'
    ]


admin.site.register(Program, ProgramAdmin)
