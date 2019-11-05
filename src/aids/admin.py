from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from aids.admin_views import AmendmentMerge
from aids.models import Aid
from aids.forms import AidAdminForm


class AidAdmin(admin.ModelAdmin):
    """Admin module for aids."""

    class Media:
        css = {
            'all': ('css/admin.css',)
        }

    form = AidAdminForm
    ordering = ['-id']
    save_as = True
    actions = ['make_mark_as_CFP']
    list_display = [
        'name', 'all_backers', 'author', 'recurrence', 'date_updated',
        'date_published', 'is_imported', 'import_uniqueid', 'status']
    autocomplete_fields = ['author', 'backers', 'perimeter']
    search_fields = ['name', 'perimeter__name', 'backers__name']
    list_filter = ['status', 'recurrence', 'is_imported',
                   'is_call_for_project']
    readonly_fields = [
        'is_imported', 'import_uniqueid', 'import_data_url',
        'import_share_licence', 'import_last_access', 'date_created',
        'date_updated', 'date_published']
    fieldsets = [
        (_('Aid presentation'), {
            'fields': (
                'name',
                'slug',
                'description',
                'tags',
                'targeted_audiances',
                'backers',
                'new_backer',
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
                'is_call_for_project',
                'aid_types',
                'subvention_rate',
                'subvention_comment',
                'mobilization_steps',
                'destinations',
                'eligibility',
            )
        }),

        (_('Contact and actions'), {
            'fields': (
                'origin_url',
                'application_url',
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

        (_('Import related data'), {
            'fields': (
                'is_imported',
                'import_uniqueid',
                'import_data_url',
                'import_share_licence',
                'import_last_access',
            )
        }),
        (_('Misc data'), {
            'fields': (
                'date_created',
                'date_updated',
                'date_published',
            )
        }),
    ]

    def get_queryset(self, request):
        qs = Aid.objects.all()
        qs = qs.prefetch_related('backers')
        qs = qs.select_related('author')
        return qs

    def all_backers(self, aid):
        backers = [backer.name for backer in aid.backers.all()]
        return ', '.join(backers)
    all_backers.short_description = _('Backers')

    def make_mark_as_CFP(self, request, queryset):
        queryset.update(is_call_for_project=True)
        self.message_user(request, _('The selected aids were set as CFP'))
    make_mark_as_CFP.short_description = _('Set as CFP')


class Amendment(Aid):
    """We need this so we can register the same model twice."""
    class Meta:
        proxy = True
        verbose_name = _('Amendment')
        verbose_name_plural = _('Amendments')


class AmendmentChangeList(ChangeList):
    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)
        url = reverse('admin:aids_amendment_merge', args=[pk])
        return url


class AmendmentAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'amended_aid', 'amendment_author_name', 'date_created'
    ]

    def get_queryset(self, request):
        qs = Aid.amendments.all()
        qs = qs.prefetch_related('backers')
        qs = qs.select_related('author')
        return qs

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(_('<path:object_id>/merge/'), self.admin_site.admin_view(
                AmendmentMerge.as_view()), name='aids_amendment_merge'),
        ]
        return my_urls + urls

    def get_changelist(self, request, **kwargs):
        return AmendmentChangeList


admin.site.register(Aid, AidAdmin)
admin.site.register(Amendment, AmendmentAdmin)
