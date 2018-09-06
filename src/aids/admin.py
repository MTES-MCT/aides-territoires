from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from aids.forms import AidAdminForm


class AidAdmin(admin.ModelAdmin):
    """Admin module for aids."""

    form = AidAdminForm
    list_display = ['name', 'author', 'backer']
    autocomplete_fields = ['author', 'backer', 'perimeter']
    search_fields = ['name']
    fieldsets = [
        (None, {
            'fields': (
                'name',
                'description',
                'backer',
                'author',
                'status',
            )
        }),

        (_('Calendar'), {
            'fields': (
                'recurrence',
                'start_date',
                'predeposit_date',
                'submission_deadline',
            )
        }),

        (_('Perimeter'), {
            'fields': (
                'perimeter',
            )
        }),

        (_('Aid description'), {
            'fields': (
                'aid_types',
                'mobilization_steps',
                'destinations',
                'thematics',
                'keywords',
                'targeted_audiances',
                'eligibility',
            )
        }),

        (_('Misc.'), {
            'fields': (
                'url',
                'contact_detail',
                'contact_email',
                'contact_phone',
            )
        }),
    ]


admin.site.register(Aid, AidAdmin)
