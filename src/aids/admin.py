from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from aids.forms import AidAdminForm


class AidAdmin(admin.ModelAdmin):
    """Admin module for aids."""

    form = AidAdminForm
    list_display = ['name', 'author', 'backer']
    autocomplete_fields = ['author', 'backer']
    fieldsets = [
        (None, {
            'fields': (
                'name',
                'description',
                'author',
                'backer',
                'status',
            )
        }),

        (_('Aid description'), {
            'fields': (
                'is_funding',
                'aid_types',
                'aid_types_detail',
                'mobilization_steps',
                'destinations',
                'destinations_detail',
                'thematics',
                'subvention_rate',
                'keywords',

            )
        }),

        (_('Eligibility'), {
            'fields': (
                'eligibility',
                'application_perimeter',
                'application_region',
                'application_department',
                'targeted_audiances',
                'targeted_audiances_detail',
                'minimal_population',
                'maximal_population',
                'open_to_third_party',
            )
        }),

        (_('Contact'), {
            'fields': (
                'url',
                'contact_email',
                'contact_phone',
                'contact_detail'
            )
        }),


        (_('Calendar'), {
            'fields': (
                'publication_status',
                'start_date',
                'predeposit_date',
                'submission_deadline',
            )
        })
    ]


admin.site.register(Aid, AidAdmin)
