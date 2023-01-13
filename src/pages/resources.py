from django.db.models.fields import TextField, CharField, URLField

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from programs.models import Program
from pages.models import FaqQuestionAnswer, FaqCategory
from stats.utils import log_event


class FaqQuestionAnswerResource(resources.ModelResource):
    """Resource for Import-export."""

    # custom widgets to ForeignKey/ManyToMany information instead of ids
    faq_category = fields.Field(
        column_name="faq_category",
        attribute="faq_category",
        widget=ForeignKeyWidget(FaqCategory, field="name"),
    )
    program = fields.Field(
        column_name="program",
        attribute="program",
        widget=ForeignKeyWidget(Program, field="name"),
    )

    class Meta:
        model = FaqQuestionAnswer
        import_id_fields = ("id",)
        # adding custom widgets breaks the usual order
        export_order = [field.name for field in FaqQuestionAnswer._meta.fields]

    def get_import_fields(self):
        return [field for field in self.get_fields()]

    def get_user_visible_fields(self):
        return [field for field in self.get_fields()]

    def before_import_row(self, row, row_number=None, **kwargs):
        """
        Why do we need to override before_import_row() ?
        - to revert the translation of row keys (header)
        - to clean/set some values
        """

        # rename keys
        for key in list(row.keys()):
            for field in (
                FaqQuestionAnswer._meta.model._meta.fields
                + FaqQuestionAnswer._meta.model._meta.many_to_many
            ):
                if field.verbose_name == key:
                    row[field.name] = row[key]
                    del row[key]
        # add/set keys

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        """
        Why do we need to override import_field() ?
        - avoid None in text fields
        - avoid empty string in lists & relations
        - revert the translation of some specific fields
        """
        if field.attribute and field.column_name in data:
            field_model = FaqQuestionAnswer._meta.get_field(field.column_name)
            # avoid None for fields text fields (happens from xlsx)
            if type(field_model) in [TextField, CharField, URLField]:
                data[field.column_name] = data.get(field.column_name, "") or ""
            # keep linebreaks in TextField columns
            if type(field_model) == TextField:
                data[field.column_name] = data[field.column_name].replace(
                    "\n", "<br />\n"
                )
            # avoid empty string for fields with base_field
            if hasattr(field_model, "base_field") and not data[field.column_name]:
                data[field.column_name] = None
            field.save(obj, data, is_m2m, **kwargs)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if not dry_run:
            file_name = kwargs.get("file_name", "nom du fichier inconnu")
            success_message = "{} questions-réponses total, {} questions-réponses crées, \
             {} questions-réponses maj".format(
                result.total_rows, result.totals["new"], result.totals["update"]
            )
            log_event(
                "FaqQuestionAnswer",
                "import_xlsx_csv",
                meta=success_message,
                source=file_name,
                value=result.total_rows,
            )
