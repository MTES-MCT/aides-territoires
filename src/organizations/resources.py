from import_export import fields, resources

from projects.models import Project
from organizations.models import Organization


ORGANIZATION_EXPORT_FIELDS = (
    'id',
    'name',
    'organization_type',
    'address',
    'city_name',
    'zip_code',
    'perimeter',
    'perimeter_region',
    'perimeter_department',
    'beneficiaries',
    'projects'
)


class OrganizationResource(resources.ModelResource):
    """Resource for Import-export."""

    beneficiaries = fields.Field(
        column_name='Utilisateurs liés',
    )

    projects = fields.Field(
        column_name="Projets de l'organisation",
    )

    perimeter = fields.Field(
        column_name="Périmètre de l'organisation",
    )

    perimeter_region = fields.Field(
        column_name="Code Région du Périmètre",
    )

    perimeter_department = fields.Field(
        column_name="Code Département du Périmètre",
    )

    def dehydrate_beneficiaries(self, obj):
        if obj.beneficiaries:
            beneficiaries_list = []
            for beneficiary in obj.beneficiaries.all():
                beneficiaries_list.append(beneficiary.full_name)
        if beneficiaries_list == []:
            return ''
        else:
            return ', '.join(beneficiaries_list)

    def dehydrate_perimeter(self, obj):
        if obj.perimeter:
            return obj.perimeter.name
        else:
            return ''

    def dehydrate_perimeter_region(self, obj):
        if obj.perimeter:
            if obj.perimeter.regions:
                return obj.perimeter.regions[0]
        else:
            return ''

    def dehydrate_perimeter_department(self, obj):
        if obj.perimeter:
            if obj.perimeter.departments:
                return obj.perimeter.departments[0]
        else:
            return ''

    def dehydrate_projects(self, obj):
        projects_list = []
        projects = Project.objects.filter(organizations=obj)
        for project in projects:
            projects_list.append(project.name)

        if projects_list == []:
            return ''
        else:
            return ', '.join(projects_list)

    class Meta:
        model = Organization
        skip_unchanged = True
        # name must be unique
        import_id_fields = ('id',)
        fields = ORGANIZATION_EXPORT_FIELDS
        export_order = ORGANIZATION_EXPORT_FIELDS

    def get_export_headers(self):
        """override get_export_headers() to translate field names."""
        headers = []
        meta_field_names = []
        for field in Organization._meta.get_fields():
            meta_field_names.append(field.name)

        for export_field in self.get_export_fields():
            if export_field.column_name in meta_field_names:
                field_model = Organization._meta.get_field(export_field.column_name)
                headers.append(field_model.verbose_name)
            else:
                headers.append(export_field.column_name)
        return headers

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, 'dehydrate_%s' % field_name, None)
        if method is not None:
            return method(obj)

        field_model = Organization._meta.get_field(field.column_name)
        if field_model.serialize:
            # simple fields with choices: use get_FOO_display to translate
            if field_model.choices:
                value = getattr(obj, f'get_{field.column_name}_display')()
                if value is not None:
                    return field.widget.render(value, obj)
            # ChoiceArrayField fields: need to translate a list
            elif hasattr(field_model, 'base_field') and field_model.base_field.choices:  # noqa
                value_raw = field.get_value(obj)
                if value_raw:
                    # translate each dict choice
                    value = [dict(field_model.base_field.choices).get(value, value) for value in value_raw]  # noqa
                    return field.widget.render(value, obj)
            # BooleanField fields: avoid returning 1 (True) and 0 (False)
            elif field_model.get_internal_type() == 'BooleanField':
                value_raw = field.get_value(obj)
                if value_raw is not None:
                    return 'Oui' if value_raw else 'Non'

        return field.export(obj)
