from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget


from projects.models import Project, ValidatedProject
from organizations.models import Organization


class ProjectResource(resources.ModelResource):

    organizations = fields.Field(
        column_name="organizations",
        attribute="organizations",
        widget=ManyToManyWidget(Organization, field="name"),
    )

    class Meta:
        model = Project
        import_id_fields = ("slug",)
        fields = ("name", "organizations", "description", "date_created", "is_public")
        export_order = ("name", "organizations", "description")

    perimeter = fields.Field(
        column_name="Périmètre du porteur de projet",
    )

    perimeter_region = fields.Field(
        column_name="Périmètre (Région)",
    )

    perimeter_department = fields.Field(
        column_name="Périmètre (Département)",
    )

    def dehydrate_perimeter(self, obj):
        if obj.organizations.all():
            if obj.organizations.first().perimeter:
                return obj.organizations.first().perimeter.name
        else:
            return ""

    def dehydrate_perimeter_region(self, obj):
        if obj.organizations.all():
            if obj.organizations.first().perimeter:
                if obj.organizations.first().perimeter.regions:
                    return obj.organizations.first().perimeter.regions[0]
        else:
            return ""

    def dehydrate_perimeter_department(self, obj):
        if obj.organizations.all():
            if obj.organizations.first().perimeter:
                if obj.organizations.first().perimeter.departments:
                    return obj.organizations.first().perimeter.departments[0]
        else:
            return ""

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, "dehydrate_%s" % field_name, None)
        if method is not None:
            return method(obj)

        field_model = Project._meta.get_field(field.column_name)
        if field_model.serialize:
            # simple fields with choices: use get_FOO_display to translate
            if field_model.choices:
                value = getattr(obj, f"get_{field.column_name}_display")()
                return field.widget.render(value, obj)
            # ChoiceArrayField fields: need to translate a list
            elif (
                hasattr(field_model, "base_field") and field_model.base_field.choices
            ):  # noqa
                value_raw = field.get_value(obj)
                if value_raw:
                    # translate each dict choice
                    value = [
                        dict(field_model.base_field.choices).get(value, value)
                        for value in value_raw
                    ]  # noqa
                    return field.widget.render(value, obj)
            # BooleanField fields: avoid returning 1 (True) and 0 (False)
            elif field_model.get_internal_type() == "BooleanField":
                value_raw = field.get_value(obj)
                if value_raw is not None:
                    return "Oui" if value_raw else "Non"

        return field.export(obj)


class ValidatedProjectResource(resources.ModelResource):
    organization_name = fields.Field(
        column_name="organization_name",
        attribute="organization",
        widget=ForeignKeyWidget(Organization, field="name"),
    )

    organization_insee = fields.Field(
        column_name="organization_insee",
        attribute="organization",
        widget=ForeignKeyWidget(Organization, field="perimeter__code"),
    )

    class Meta:
        model = ValidatedProject
        import_id_fields = ("import_uniqueid",)
        fields = (
            "project_name",
            "project_linked",
            "description",
            "aid_name",
            "aid_linked",
            "organization_name",
            "organization_insee",
            "financer_linked",
            "financer_name",
            "budget",
            "amount_obtained",
            "date_obtained",
            "date_created",
        )
