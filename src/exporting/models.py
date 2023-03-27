from django.db import models


class DataExport(models.Model):
    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        verbose_name="Auteur",
        limit_choices_to={"is_superuser": True},
        help_text="La personne qui a déclenché l’export",
    )
    exported_file = models.FileField("fichier exporté", upload_to="data-export")
    date_created = models.DateTimeField("Date de création", auto_now_add=True)

    class Meta:
        verbose_name = "Export de données"
        verbose_name_plural = "Exports de données"

    def __str__(self):
        return self.exported_file.name
