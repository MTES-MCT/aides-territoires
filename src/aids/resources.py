from django.db.models.fields import TextField, CharField, URLField

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from aids.models import Aid, AidProject
from accounts.models import User
from categories.models import Category
from backers.models import Backer
from core.utils import get_base_url
from geofr.models import Perimeter
from programs.models import Program
from projects.models import Project
from stats.utils import log_event


AIDS_BOOLEAN_FIELDS = [
    "is_call_for_project",
    "in_france_relance",
    "is_imported",
]

AIDS_EXPORT_EXCLUDE_FIELDS = [
    "short_title",
    "financer_suggestion",
    "instructor_suggestion",
    "perimeter_suggestion",
    "import_uniqueid",
    "import_share_licence",
    "import_last_access",
    "search_vector",
    "is_amendment",
    "amended_aid",
    "amendment_author_name",
    "amendment_author_email",
    "amendment_author_org",
    "amendment_comment",
    "local_characteristics",
]
AIDS_IMPORT_EXCLUDE_FIELDS = [
    "slug",
    "status",
    "date_updated",
    "date_published",
    "author_notification",
    "projects",
]
AIDS_IMPORT_CLEAN_FIELDS = ["is_imported", "author", "subvention_rate"]

ADMIN_EMAIL = "admin@test.com"


class AidResource(resources.ModelResource):
    """Resource for Import-export."""

    # custom widgets to ForeignKey/ManyToMany information instead of ids
    author = fields.Field(
        column_name="author",
        attribute="author",
        widget=ForeignKeyWidget(User, field="email"),
    )
    categories = fields.Field(
        column_name="categories",
        attribute="categories",
        widget=ManyToManyWidget(Category, field="name"),
    )
    financers = fields.Field(
        column_name="financers",
        attribute="financers",
        widget=ManyToManyWidget(Backer, field="name"),
    )
    instructors = fields.Field(
        column_name="instructors",
        attribute="instructors",
        widget=ManyToManyWidget(Backer, field="name"),
    )
    perimeter = fields.Field(
        column_name="perimeter",
        attribute="perimeter",
        widget=ForeignKeyWidget(Perimeter, field="name"),
    )
    programs = fields.Field(
        column_name="programs",
        attribute="programs",
        widget=ManyToManyWidget(Program, field="name"),
    )

    class Meta:
        model = Aid
        import_id_fields = ("id",)
        exclude = AIDS_EXPORT_EXCLUDE_FIELDS
        # adding custom widgets breaks the usual order
        export_order = [
            field.name
            for field in Aid._meta.fields
            if field.name not in AIDS_EXPORT_EXCLUDE_FIELDS
        ]

    def get_import_fields(self):
        return [
            field
            for field in self.get_fields()
            if field.column_name not in AIDS_IMPORT_EXCLUDE_FIELDS
        ]

    def get_user_visible_fields(self):
        return [
            field
            for field in self.get_fields()
            if field.column_name not in AIDS_IMPORT_EXCLUDE_FIELDS
        ]

    def before_import_row(self, row, row_number=None, **kwargs):
        """
        Why do we need to override before_import_row() ?
        - to revert the translation of row keys (header)
        - to clean/set some values
        """
        # rename keys
        for key in list(row.keys()):
            for field in (
                Aid._meta.model._meta.fields + Aid._meta.model._meta.many_to_many
            ):
                if field.verbose_name == key:
                    row[field.name] = row[key]
                    del row[key]
        # remove keys
        for key in AIDS_IMPORT_EXCLUDE_FIELDS:
            if key in row:
                del row[key]
        # add/set keys
        row["author"] = row.get("author", ADMIN_EMAIL) or ADMIN_EMAIL
        row["is_imported"] = True
        if "subvention_rate" in row:
            if row["subvention_rate"]:
                row["subvention_rate"] = (
                    row["subvention_rate"].replace("(", "[").replace("None", "")
                )

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        """
        Why do we need to override import_field() ?
        - avoid None in text fields
        - avoid empty string in lists & relations
        - revert the translation of some specific fields
        """
        if field.attribute and field.column_name in data:
            field_model = Aid._meta.get_field(field.column_name)
            # avoid None for fields text fields (happens from xlsx)
            if type(field_model) in [TextField, CharField, URLField]:
                data[field.column_name] = data.get(field.column_name, "") or ""
            # keep linebreaks in TextField columns
            if type(field_model) is TextField:
                data[field.column_name] = data[field.column_name].replace(
                    "\n", "<br />\n"
                )
            # avoid empty string for fields with base_field
            if hasattr(field_model, "base_field") and not data[field.column_name]:
                data[field.column_name] = None
            # revert the translation of some specific fields
            if data[field.column_name]:
                # simple fields with choices
                if field_model.choices:
                    data[field.column_name] = next(
                        k
                        for k, v in iter(dict(field_model.flatchoices).items())
                        if v == data[field.column_name]
                    )
                # ChoiceArrayField fields
                if (
                    hasattr(field_model, "base_field")
                    and field_model.base_field.choices
                ):
                    data[field.column_name] = [
                        k
                        for k, v in iter(
                            dict(field_model.base_field.flatchoices).items()
                        )
                        if str(v) in data[field.column_name]
                    ]
                    data[field.column_name] = ",".join(data[field.column_name])
                # BooleanField fields
                if field.column_name in AIDS_BOOLEAN_FIELDS:
                    if data[field.column_name] == "Oui":
                        data[field.column_name] = True
                    elif data[field.column_name] == "Non":
                        data[field.column_name] = False
                    else:
                        data[field.column_name] = None
            field.save(obj, data, is_m2m, **kwargs)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if not dry_run:
            file_name = kwargs.get("file_name", "nom du fichier inconnu")
            success_message = "{} aides total, {} aides crées, {} aids maj".format(
                result.total_rows, result.totals["new"], result.totals["update"]
            )
            log_event(
                "aid",
                "import_xlsx_csv",
                meta=success_message,
                source=file_name,
                value=result.total_rows,
            )

    def get_export_headers(self):
        """override get_export_headers() to translate field names."""
        headers = []
        for field in self.get_export_fields():
            field_model = Aid._meta.get_field(field.column_name)
            headers.append(field_model.verbose_name)
        return headers

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, "dehydrate_%s" % field_name, None)
        if method is not None:
            return method(obj)

        field_model = Aid._meta.get_field(field.column_name)
        if field_model.serialize:
            # simple fields with choices: use get_FOO_display to translate
            if field_model.choices:
                value = getattr(obj, f"get_{field.column_name}_display")()
                return field.widget.render(value, obj)
            # For Text and Char fields, we remove illegal characters
            elif isinstance(field_model, (TextField, CharField)):
                export_value = field.export(obj)
                export_value = ILLEGAL_CHARACTERS_RE.sub("", export_value)
                return export_value
            # ChoiceArrayField fields: need to translate a list
            elif hasattr(field_model, "base_field") and field_model.base_field.choices:
                value_raw = field.get_value(obj)
                if value_raw:
                    # translate each dict choice
                    value = [
                        dict(field_model.base_field.choices).get(value, value)
                        for value in value_raw
                    ]
                    return field.widget.render(value, obj)
            # BooleanField fields: avoid returning 1 (True) and 0 (False)
            elif field_model.get_internal_type() == "BooleanField":
                value_raw = field.get_value(obj)
                if value_raw is not None:
                    return "Oui" if value_raw else "Non"

        # subvention_rate
        if field.column_name == "subvention_rate":
            if field.get_value(obj) is None:
                return ""
            else:
                lower = field.get_value(obj).lower or ""
                upper = field.get_value(obj).upper or ""
                return f"[{lower}, {upper})"
        return field.export(obj)


class AidResourcePublic(AidResource):
    """Resource for a lighter public export."""

    full_url = fields.Field(
        column_name="Adresse de la fiche aide",
    )

    class Meta:
        model = Aid

        fields = [
            "full_url",
            "name",
            "description",
            "project_examples",
            "mobilization_steps",
            "aid_types",
            "destinations",
            "start_date",
            "submission_deadline",
            "subvention_rate",
            "subvention_comment",
            "recoverable_advance_amount",
            "loan_amount",
            "other_financial_aid_comment",
            "contact",
            "recurrence",
            "is_call_for_project",
            "categories",
            "financers",
            "instructors",
            "programs",
        ]
        export_order = fields

    def get_export_order(self):
        """override to export only the fields explicited above"""
        return tuple(self._meta.export_order or ())

    def get_export_headers(self):
        """override get_export_headers() to translate field names."""
        headers = []
        meta_field_names = []
        for field in Aid._meta.get_fields():
            meta_field_names.append(field.name)

        for export_field in self.get_export_fields():
            if export_field.column_name in meta_field_names:
                field_model = Aid._meta.get_field(export_field.column_name)
                headers.append(field_model.verbose_name)
            else:
                headers.append(export_field.column_name)
        return headers

    def dehydrate_full_url(self, obj):
        base_url = get_base_url()
        return f"{base_url}{obj.get_absolute_url()}"


class AidProjectResource(resources.ModelResource):
    """Resource for Export AidProject."""

    # custom widgets to ForeignKey information instead of ids
    creator = fields.Field(
        column_name="creator",
        attribute="creator",
        widget=ForeignKeyWidget(User, field="email"),
    )
    aid = fields.Field(
        column_name="aid",
        attribute="aid",
        widget=ForeignKeyWidget(Aid, field="name"),
    )
    project = fields.Field(
        column_name="project",
        attribute="project",
        widget=ForeignKeyWidget(Project, field="name"),
    )

    class Meta:
        model = AidProject
        fields = [
            "aid",
            "project",
            "creator",
            "aid_requested",
            "aid_obtained",
            "aid_paid",
            "aid_denied",
            "date_created",
        ]
        export_order = fields

    def get_export_headers(self):
        """override get_export_headers() to translate field names."""
        headers = []
        for field in self.get_export_fields():
            field_model = AidProject._meta.get_field(field.column_name)
            headers.append(field_model.verbose_name)
        return headers

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, "dehydrate_%s" % field_name, None)
        if method is not None:
            return method(obj)

        field_model = AidProject._meta.get_field(field.column_name)
        if field_model.serialize:
            # For Text and Char fields, we remove illegal characters
            if isinstance(field_model, (TextField, CharField)):
                export_value = field.export(obj)
                export_value = ILLEGAL_CHARACTERS_RE.sub("", export_value)
                return export_value
            # BooleanField fields: avoid returning 1 (True) and 0 (False)
            elif field_model.get_internal_type() == "BooleanField":
                value_raw = field.get_value(obj)
                if value_raw is not None:
                    return "Oui" if value_raw else "Non"

        return field.export(obj)
