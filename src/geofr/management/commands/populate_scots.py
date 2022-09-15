from django.core.management.base import BaseCommand

# from geofr.services.populate_scots import populate_scots


class Command(BaseCommand):
    """Import the list of SCoTs."""

    def handle(self, *args, **options):
        print(
            """Cette commande est temporairement désactivée,
        cf. https://www.notion.so/Diminuer-la-taille-de-l-environnement-virtuel-Python-e696e339bcb0473490dd79311cc4e83c  # noqa
        """
        )
        """
        result = populate_scots()
        self.stdout.write(
            self.style.SUCCESS(
                f"{result['created']} created, {result['updated']} \
                    updated, {result['obsolete']} obsolete."
            )
        )
        """
