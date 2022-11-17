from import_export import fields, resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from backers.models import BackerGroup, Backer


BACKER_IMPORT_FIELDS = ("name",)
BACKER_EXPORT_FIELDS = (
    "id",
    "name",
    "slug",
    "group",
    "nb_financed_aids",
    "nb_instructed_aids",
)


class BackerResource(resources.ModelResource):
    """Resource for Import-export."""

    group = fields.Field(
        column_name="group",
        attribute="group",
        widget=ForeignKeyWidget(BackerGroup, field="name"),
    )
    nb_financed_aids = Field(column_name="nb_financed_aids")
    nb_instructed_aids = Field(column_name="nb_instructed_aids")

    def dehydrate_nb_financed_aids(self, obj):
        return obj.nb_financed_aids

    def dehydrate_nb_instructed_aids(self, obj):
        return obj.nb_instructed_aids

    class Meta:
        model = Backer
        skip_unchanged = True
        # name must be unique
        import_id_fields = ("name",)
        fields = BACKER_EXPORT_FIELDS
        export_order = BACKER_EXPORT_FIELDS

    def get_import_fields(self):
        return [
            field
            for field in self.get_fields()
            if field.column_name in BACKER_IMPORT_FIELDS
        ]  # noqa

    def get_user_visible_fields(self):
        return [
            field
            for field in self.get_fields()
            if field.column_name in BACKER_IMPORT_FIELDS
        ]  # noqa
