from django.utils.translation import gettext_lazy as _

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from projects.models import Project


PROJECTS_EXPORT_EXCLUDE_FIELDS = [
    'id', 'is_suggested', 'status', 'slug'
]


class ProjectResource(resources.ModelResource):
    """Resource for Import-export."""

    # custom widgets to ForeignKey/ManyToMany information instead of ids
    categories = fields.Field(
        column_name='categories',
        attribute='categories',
        widget=ManyToManyWidget('categories.Category', field='name')
    )

    class Meta:
        model = Project
        exclude = PROJECTS_EXPORT_EXCLUDE_FIELDS
        # adding custom widgets breaks the usual order
        export_order = [field.name for field in Project._meta.fields if field.name not in PROJECTS_EXPORT_EXCLUDE_FIELDS]  # noqa

    def get_export_headers(self):
        """override get_export_headers() to translate field names."""
        headers = []
        for field in self.get_export_fields():
            field_model = self.Meta.model._meta.get_field(field.column_name)
            headers.append(field_model.verbose_name)
        return headers

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, 'dehydrate_%s' % field_name, None)
        if method is not None:
            return method(obj)

        field_model = self.Meta.model._meta.get_field(field.column_name)
        if field_model.serialize:
            # simple fields with choices: use get_FOO_display to translate
            if field_model.choices:
                value = getattr(obj, f'get_{field.column_name}_display')()
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
                    return _('Yes') if value_raw else _('No')
        return field.export(obj)
