from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from accounts.models import User
from organizations.models import Organization


USER_IMPORT_FIELDS = ("name",)
USER_EXPORT_FIELDS = (
    "id",
    "first_name",
    "last_name",
    "email",
    "contributor_contact_phone",
    "perimeter",
    "perimeter_region",
    "perimeter_department",
    "is_contributor",
    "is_beneficiary",
    "nb_aids",
    "beneficiary_organization",
    "beneficiary_organization_id",
    "beneficiary_organization_projects_count",
    "beneficiary_organization_projects_have_aids",
    "contributor_organization",
    "beneficiary_function",
    "contributor_role",
    "beneficiary_role",
    "date_created",
    "date_updated",
    "last_login",
)


class UserResource(resources.ModelResource):
    """Resource for Import-export."""

    beneficiary_organization = fields.Field(
        column_name="beneficiary_organization",
        attribute="beneficiary_organization",
        widget=ForeignKeyWidget(Organization, field="name"),
    )

    beneficiary_organization_id = fields.Field(
        column_name="ID de l'organisation",
    )

    beneficiary_organization_projects_count = fields.Field(
        column_name="Nombre de projets de l'organisation",
    )

    beneficiary_organization_projects_have_aids = fields.Field(
        column_name="Présence d'aides associées à un projet",
    )

    perimeter = fields.Field(
        column_name="Périmètre de l'organisation",
    )

    perimeter_region = fields.Field(
        column_name="Périmètre (Région)",
    )

    perimeter_department = fields.Field(
        column_name="Périmètre (Département)",
    )

    nb_aids = fields.Field(
        column_name="Nombre d'aides",
    )

    org_type = fields.Field(
        column_name="Type de structure",
    )

    org_zipcode = fields.Field(
        column_name="Code postal de la structure",
    )

    def dehydrate_beneficiary_organization_projects_count(self, obj):
        if obj.beneficiary_organization:
            if obj.beneficiary_organization.project_set:
                return obj.beneficiary_organization.project_set.count()
        else:
            return ""

    def dehydrate_beneficiary_organization_projects_have_aids(self, obj):
        if obj.beneficiary_organization:
            if obj.beneficiary_organization.project_set:
                for project in obj.beneficiary_organization.project_set.all():
                    if project.aid_set.all().count() > 0:
                        return True

    def dehydrate_beneficiary_organization_id(self, obj):
        if obj.beneficiary_organization:
            return obj.beneficiary_organization.id
        else:
            return ""

    def dehydrate_org_zipcode(self, obj):
        if obj.beneficiary_organization:
            return obj.beneficiary_organization.zip_code
        else:
            return ""

    def dehydrate_org_type(self, obj):
        if obj.beneficiary_organization:
            return obj.beneficiary_organization.organization_type[0]
        else:
            return ""

    def dehydrate_perimeter(self, obj):
        if obj.beneficiary_organization:
            if obj.beneficiary_organization.perimeter:
                return obj.beneficiary_organization.perimeter.name
        else:
            return ""

    def dehydrate_perimeter_region(self, obj):
        if obj.beneficiary_organization:
            if obj.beneficiary_organization.perimeter:
                if obj.beneficiary_organization.perimeter.regions:
                    return obj.beneficiary_organization.perimeter.regions[0]
        else:
            return ""

    def dehydrate_perimeter_department(self, obj):
        if obj.beneficiary_organization:
            if obj.beneficiary_organization.perimeter:
                if obj.beneficiary_organization.perimeter.departments:
                    return obj.beneficiary_organization.perimeter.departments[0]
        else:
            return ""

    def dehydrate_nb_aids(self, obj):
        return obj.aids.count()

    class Meta:
        model = User
        skip_unchanged = True
        # name must be unique
        import_id_fields = ("id",)
        fields = USER_EXPORT_FIELDS
        export_order = USER_EXPORT_FIELDS

    def get_export_headers(self):
        """override get_export_headers() to translate field names."""
        headers = []
        meta_field_names = []
        for field in User._meta.get_fields():
            meta_field_names.append(field.name)

        for export_field in self.get_export_fields():
            if export_field.column_name in meta_field_names:
                field_model = User._meta.get_field(export_field.column_name)
                headers.append(field_model.verbose_name)
            else:
                headers.append(export_field.column_name)
        return headers

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, "dehydrate_%s" % field_name, None)
        if method is not None:
            return method(obj)

        field_model = User._meta.get_field(field.column_name)
        if field_model.serialize:
            # simple fields with choices: use get_FOO_display to translate
            if field_model.choices:
                value = getattr(obj, f"get_{field.column_name}_display")()
                if value is not None:
                    return field.widget.render(value, obj)
            # BooleanField fields: avoid returning 1 (True) and 0 (False)
            elif field_model.get_internal_type() == "BooleanField":
                value_raw = field.get_value(obj)
                if value_raw is not None:
                    return "Oui" if value_raw else "Non"

        return field.export(obj)
