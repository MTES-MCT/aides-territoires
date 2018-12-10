from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from aids.models import Aid
from aids.forms import AidAdminForm


class AidAdmin(admin.ModelAdmin):
    """Admin module for aids."""

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    form = AidAdminForm
    save_as = True
    list_display = ['name', 'all_backers', 'author', 'recurrence',
                    'date_updated', 'is_imported', 'status']
    autocomplete_fields = ['author', 'backers', 'perimeter']
    search_fields = ['name']
    list_filter = ['status', 'recurrence', 'is_imported']
    fieldsets = [
        (_('Aid presentation'), {
            'fields': (
                'name',
                'slug',
                'description',
                'tags',
                'targeted_audiances',
                'backers',
                'author',
            )
        }),

        (_('Aid perimeter'), {
            'fields': (
                'perimeter',
            )
        }),

        (_('Aid calendar'), {
            'fields': (
                'recurrence',
                'start_date',
                'predeposit_date',
                'submission_deadline',
            )
        }),

        (_('Aid description'), {
            'fields': (
                'aid_types',
                'subvention_rate',
                'mobilization_steps',
                'destinations',
                'eligibility',
            )
        }),

        (_('Contact and actions'), {
            'fields': (
                'application_url',
                'url',
                'contact_detail',
                'contact_email',
                'contact_phone',
            )
        }),

        (_('Aid admin'), {
            'fields': (
                'status',
            )
        }),
    ]

    def get_queryset(self, request):
        qs = Aid.all_aids.all()
        qs = qs.prefetch_related('backers')
        qs = qs.select_related('author')
        return qs

    def all_backers(self, aid):
        backers = [backer.name for backer in aid.backers.all()]
        return ', '.join(backers)
    all_backers.short_description = _('Backers')


admin.site.register(Aid, AidAdmin)
