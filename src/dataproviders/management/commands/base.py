import scrapy
from scrapy.crawler import CrawlerProcess

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import CharField, TextField
from django.utils import timezone

from aids.models import Aid
from aids.forms import AidEditForm
from stats.utils import log_event


# Call for projects will often contain those words
AAP_SYNONYMS = [
    'appel à projet',
    'appel a projet',
    'aap',
    'appel à manifestation',
    'appel a manifestation',
    'ami',
]

# The first user in the db is the admin
ADMIN_ID = 1


class BaseImportCommand(BaseCommand):
    """Base data import command.

    This base commands, meant to be inherited, provides a common structure
    for all commands that import aid data from third-party providers (Ademe,
    Dreal, etc.)
    """

    def populate_cache(self, *args, **options):
        pass

    def handle(self, *args, **options):
        self.populate_cache(*args, **options)
        data = self.fetch_data(**options)
        aids_and_related_objects = []
        for line in data:
            if self.line_should_be_processed(line):
                aids_and_related_objects.append(self.process_line(line))

        # Let's try to actually save the imported aid.
        #
        # For each aid, we have two cases:
        #   1) The aid is actually new, so we just create it.
        #   2) The aid is known from a previous import, in that case,
        #      we just update a few fields but we don't overwrite some
        #      manual modifications that could have been made from our side.
        created_counter = 0
        updated_counter = 0
        with transaction.atomic():
            for aid, financers, instructors, categories, programs in aids_and_related_objects:  # noqa
                try:
                    with transaction.atomic():
                        aid.set_search_vector_unaccented(financers, instructors, categories)
                        aid.save()
                        aid.financers.set(financers)
                        aid.instructors.set(instructors)
                        aid.categories.set(categories)
                        aid.programs.set(programs)
                        created_counter += 1
                        self.stdout.write(self.style.SUCCESS(
                            'New aid: {}'.format(aid.name)))

                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(str(e)))
                    try:
                        aid_object = Aid.objects \
                            .filter(import_uniqueid=aid.import_uniqueid)
                        if aid_object.values('import_raw_object', flat=True) != aid.import_raw_object:
                            '''
                            Si d'autres champ que : 
                                - aid.submission_deadline,
                                - aid.start_date,
                                - aid.name_initial 
                            ont été modifiés.
                            Alors on ne veut pas que l'aide soit mise à jour automatiquement. 
                            On passe donc le statut de l'aide en brouillon et on met simplement
                            à jour les champs du calendrier, plus les champs de données brutes :
                                - import_raw_object_temp et
                                - import_raw_object_temp_calendar
                                - start_date
                                - submission_deadline
                                - name_initial
                            '''
                            try:
                                aid_object \
                                    .update(
                                        start_date=aid.start_date,
                                        submission_deadline=aid.submission_deadline,
                                        name_initial=aid.name_initial,
                                        import_raw_object_temp=aid.import_raw_object,
                                        import_raw_object_temp_calendar=aid.import_raw_object_calendar,
                                        date_updated=timezone.now(),
                                        import_last_access=timezone.now(),
                                        status=draft)
                                updated_counter += 1
                                self.stdout.write(self.style.SUCCESS(
                                    'Updated aid: {}'.format(aid.name)))

                            except Exception as e:
                                self.stdout.write(self.style.ERROR(
                                    'Cannot update aid {}: {}'.format(aid.name, e)))

                            '''
                            Si les seuls champs qui ont changé sont : 
                                - aid.submission_deadline,
                                - aid.start_date,
                                - aid.name_initial,
                            Alors on tente une mise à jour de ces champs.
                            On met aussi à jour le champ import_raw_object_temp_calendar
                            Le statut de l'aide doit rester 'published'. 
                            '''
                        elif aid_object.values('import_raw_object_calendar', flat=True) != aid.import_raw_object_calendar:
                            try: 
                                aid_object \
                                    .update(
                                        start_date=aid.start_date,
                                        submission_deadline=aid.submission_deadline,
                                        name_initial=aid.name_initial,
                                        import_raw_object_temp_calendar=aid.import_raw_object_calendar,
                                        date_updated=timezone.now(),
                                        import_last_access=timezone.now(),
                                        status=published)
                                updated_counter += 1
                                self.stdout.write(self.style.SUCCESS(
                                    'Updated aid: {}'.format(aid.name)))

                            except Exception as e:
                                self.stdout.write(self.style.ERROR(
                                    'Cannot update aid {}: {}'.format(aid.name, e)))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            'Cannot import aid {}: {}'.format(aid.name, e)))

        success_message = '{} aides total, {} aides crées, {} aids maj'.format(
            len(aids_and_related_objects), created_counter, updated_counter)
        self.stdout.write(self.style.SUCCESS(success_message))

        # log the results (works only for DataSource imports)
        try:
            data_source_name = aids_and_related_objects[0][0].import_data_source.name
            log_event('aid', 'import_api', meta=success_message, source=data_source_name, value=len(aids_and_related_objects))  # noqa
        except:  # noqa
            pass

    def fetch_data(self):
        """Download and / or parse the data file.

        Must return an iterator.
        """
        raise NotImplementedError

    def line_should_be_processed(self, line):
        return True

    def process_line(self, line):
        """Process a single entry from the data file.

        The Aid object MUST not be created.

        Returns the aid and all associated objects (m2m).
        """
        form_fields = AidEditForm.Meta.fields
        more_fields = [
            'author_id',
            'import_data_source', 'is_imported', 'import_uniqueid',
            'import_data_url', 'import_share_licence', 'import_last_access',
            'import_raw_object',
            'date_published'
        ]
        fields = form_fields + more_fields

        values = {
            'is_imported': True,
            'author_notification': False
        }
        for field in fields:
            extract_method_name = 'extract_{}'.format(field)
            extract_method = getattr(self, extract_method_name, None)
            model_field = Aid._meta.get_field(field)
            is_text_type = isinstance(model_field, (CharField, TextField))
            empty_value = '' if is_text_type else None
            value = extract_method(line) if extract_method else empty_value
            values[field] = value

        financers = values.pop('financers', [])
        instructors = values.pop('instructors', [])
        categories = values.pop('categories', [])
        programs = values.pop('programs', [])
        aid = Aid(**values)

        return aid, financers, instructors, categories, programs

    def extract_is_imported(self, line):
        return True

    def extract_author_id(self, line):
        return ADMIN_ID

    def extract_import_data_source(self, line):
        # raise NotImplementedError
        return None

    def extract_import_uniqueid(self, line):
        """Must return an unique import reference.

        This value is useful if we want to know if the current line
        was already processed and imported or not.
        """
        raise NotImplementedError

    def extract_import_data_url(self, line):
        raise NotImplementedError

    def extract_import_share_licence(self, line):
        raise NotImplementedError

    def extract_import_last_access(self, line):
        return timezone.now()

    def extract_name(self, line):
        raise NotImplementedError

    def extract_contact(self, line):
        return ''

    def extract_is_call_for_project(self, line):
        is_call_for_project = False
        title = self.extract_name(line).lower()
        for synonym in AAP_SYNONYMS:
            if synonym in title:
                is_call_for_project = True
                break

        return is_call_for_project

    def extract_instructors(self, line):
        return []

    def extract_categories(self, line):
        return []

    def extract_programs(self, line):
        return []

    def extract_project_examples(self, line):
        return ''

    def extract_in_france_relance(self, line):
        return False

    def extract_name_initial(self, line):
        return ''


class CrawlerImportCommand(BaseImportCommand):
    """An import task that uses a crawler to fetch data."""

    def fetch_data(self, **options):
        results = []
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'LOG_LEVEL': 'INFO',
        })
        process.crawl(self.SPIDER_CLASS)

        def add_to_results(item, response, spider):
            results.append(item)

        for p in process.crawlers:
            p.signals.connect(
                add_to_results, signal=scrapy.signals.item_scraped)
        process.start()

        for result in results:
            yield result
