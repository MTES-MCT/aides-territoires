from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import CharField
from django.utils import timezone

from aids.models import Aid
from aids.forms import AidEditForm


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
        aid_and_backers = []
        for line in data:
            if self.line_should_be_processed(line):
                aid_and_backers.append(self.process_line(line))

        # Let's try to actually save the imported aid.
        #
        # For each aid, we have two cases:
        #   1) The aid is actually new, so we just create it.
        #   2) The aid is known from a previous import, in that case,
        #      we just update a few fields but we don't overwrite some
        #      manual modifications that could have been made from our side.
        #
        # For the moment, since the data is not huge (there are probably a few
        # dozains aids per provider at best), I decided to focus on code
        # readability and not to focus on optimizing the number of db queries.
        created_counter = 0
        updated_counter = 0
        with transaction.atomic():
            for aid, backers in aid_and_backers:
                try:
                    with transaction.atomic():
                        aid.set_search_vector(backers)
                        aid.save()
                        aid.backers.set(backers)
                        aid.populate_tags()
                        created_counter += 1
                        self.stdout.write(self.style.SUCCESS(
                            'New aid: {}'.format(aid.name)))

                except IntegrityError:
                    Aid.objects \
                        .filter(import_uniqueid=aid.import_uniqueid) \
                        .update(
                            origin_url=aid.origin_url,
                            start_date=aid.start_date,
                            submission_deadline=aid.submission_deadline,
                            date_updated=timezone.now(),
                            import_last_access=timezone.now())
                    updated_counter += 1
                    self.stdout.write(self.style.SUCCESS(
                        'Updated aid: {}'.format(aid.name)))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        'Cannot import aid {}: {}'.format(aid.name, e)))

        self.stdout.write(self.style.SUCCESS(
            '{} aids created, {} aids updated'.format(
                created_counter, updated_counter)))

    def fetch_data(self):
        """Download and / or parse the data file.

        Must return an iterator.
        """
        raise NotImplementedError

    def line_should_be_processed(self, line):
        return True

    def process_line(self, line):
        """Process a single entry from the data file.

        Must return an (Aid, [Backer]) tuple.

        The Aid object MUST not be created.

        """
        form_fields = AidEditForm.Meta.fields
        more_fields = [
            'author_id', 'is_imported', 'import_uniqueid', 'import_data_url',
            'import_share_licence', 'import_last_access'
        ]
        fields = form_fields + more_fields

        values = {
            'is_imported': True
        }
        for field in fields:
            extract_method_name = 'extract_{}'.format(field)
            extract_method = getattr(self, extract_method_name, None)
            model_field = Aid._meta.get_field(field)
            empty_value = '' if isinstance(model_field, CharField) else None
            value = extract_method(line) if extract_method else empty_value
            values[field] = value

        backers = values.pop('backers', [])
        aid = Aid(**values)

        return aid, backers

    def extract_is_imported(self, line):
        return True

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

    def extract_tags(self, line):
        return []
