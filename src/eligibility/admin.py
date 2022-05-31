from django import forms
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.utils.html import format_html

from adminsortable2.admin import SortableInlineAdminMixin

from core.forms import RichTextField
from eligibility.models import EligibilityTest, EligibilityQuestion
from eligibility.tasks import export_eligibility_tests_stats_as_csv
from exporting.utils import get_admin_export_message
from accounts.admin import AuthorFilter


class EligibilityTestForm(forms.ModelForm):
    introduction = RichTextField(
        label='Une introduction',
        required=False)
    conclusion_success = RichTextField(
        label='Une conclusion si le test est positif',
        required=False)
    conclusion_failure = RichTextField(
        label='Une conclusion si le test est négatif',
        required=False)
    conclusion = RichTextField(
        label='Une conclusion générale',
        required=False)

    class Meta:
        model = EligibilityTest
        fields = '__all__'


class EligibilityQuestionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = EligibilityTest.questions.through
    extra = 1


class EligibilityTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'nb_aids', 'nb_results',
                    'date_created']
    search_fields = ['name']
    list_filter = [AuthorFilter]
    actions = ['export_csv', 'export_csv_background']

    form = EligibilityTestForm
    inlines = [EligibilityQuestionInline]
    readonly_fields = ['author', 'date_created', 'date_updated',
                       'display_related_aids']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('author') \
               .annotate(aid_count=Count('aids', distinct=True)) \
               .annotate(result_count=Count('aideligibilitytestevent', distinct=True))  # noqa
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def nb_aids(self, eligibility_test):
        return eligibility_test.aid_count
    nb_aids.short_description = "Nombre d'aides"
    nb_aids.admin_order_field = 'aid_count'

    def nb_results(self, eligibility_test):
        return eligibility_test.result_count
    nb_results.short_description = "Nombre de résultats"
    nb_results.admin_order_field = 'result_count'

    def display_related_aids(self, obj):
        related_aid_html = format_html('<table> \
            <thead><tr> \
            <th>Auteur</th> \
            <th>Aide</th> \
            </tr></thead> \
            <tbody>')
        related_aids = obj.aids.all().order_by('name').select_related('author')  # noqa
        for aid in related_aids:
            url = reverse("admin:aids_aid_change", args=(aid.pk,))
            related_aid_html += format_html(
                '<tr> \
                    <td>{author}</td> \
                    <td><a href="{url}">{name} (ID : {id})</a></td> \
                </tr>',
                url=url,
                name=aid.name,
                id=aid.pk,
                author=aid.author
            )
        related_aid_html += format_html('</tbody></table>')
        return related_aid_html
    display_related_aids.short_description = 'Aides associées'

    def show_export_message(self, request):
        self.message_user(request, get_admin_export_message())

    def export_csv(self, request, queryset):
        eligibility_tests_id_list = list(queryset.values_list('id', flat=True))
        return export_eligibility_tests_stats_as_csv(eligibility_tests_id_list, request.user.id, background=False)  # noqa
    export_csv.short_description = 'Exporter le premier Test sélectionné en CSV'  # noqa

    def export_csv_background(self, request, queryset):
        eligibility_tests_id_list = list(queryset.values_list('id', flat=True))
        export_eligibility_tests_stats_as_csv.delay(eligibility_tests_id_list, request.user.id)  # noqa
        self.show_export_message(request)
    export_csv_background.short_description = 'Exporter le premier Test sélectionné en CSV en tâche de fond'  # noqa

    class Media:
        css = {
            'all': (
                'css/admin.css',
                '/static/trumbowyg/dist/ui/trumbowyg.css',
            )
        }
        js = [
            'admin/js/jquery.init.js',
            '/static/js/shared_config.js',
            '/static/js/plugins/softmaxlength.js',
            '/static/js/search/enable_softmaxlength.js',
            '/static/trumbowyg/dist/trumbowyg.js',
            '/static/trumbowyg/dist/langs/fr.js',
            '/static/trumbowyg/dist/plugins/upload/trumbowyg.upload.js',
            '/static/trumbowyg/dist/plugins/resizimg/resizable-resolveconflict.js',  # noqa
            '/static/jquery-resizable-dom/dist/jquery-resizable.js',
            '/static/trumbowyg/dist/plugins/resizimg/trumbowyg.resizimg.js',
            '/static/js/enable_rich_text_editor.js',
        ]


class EligibilityQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'nb_tests', 'date_created']
    search_fields = ['text']
    list_filter = [AuthorFilter]
    readonly_fields = ['author', 'date_created', 'date_updated',
                       'display_related_tests']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('author') \
               .prefetch_related('eligibility_tests') \
               .annotate(test_count=Count('eligibility_tests'))
        return qs

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def nb_tests(self, eligibility_question):
        return eligibility_question.test_count
    nb_tests.short_description = 'Nombre de tests'
    nb_tests.admin_order_field = 'test_count'

    def display_related_tests(self, obj):
        related_test_html = format_html('<table> \
            <thead><tr> \
            <th>Auteur</th> \
            <th>Test d’éligibilité</th> \
            </tr></thead> \
            <tbody>')
        related_tests = obj.eligibility_tests.all().order_by('name').select_related('author')  # noqa
        for test in related_tests:
            url = reverse("admin:eligibility_eligibilitytest_change", args=(test.pk,))  # noqa
            related_test_html += format_html(
                '<tr> \
                    <td>{author}</td> \
                    <td><a href="{url}">{name} (ID : {id})</a></td> \
                </tr>',
                url=url,
                name=test.name,
                id=test.pk,
                author=test.author
            )
        related_test_html += format_html('</tbody></table>')
        return related_test_html
    display_related_tests.short_description = 'Tests associés'


admin.site.register(EligibilityTest, EligibilityTestAdmin)
admin.site.register(EligibilityQuestion, EligibilityQuestionAdmin)
