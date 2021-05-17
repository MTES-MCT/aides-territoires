from django.utils.translation import gettext_lazy as _
from django.db.models.fields import TextField, CharField, URLField

from import_export import fields, resources
from import_export.widgets import ManyToManyWidget

from projects.models import Project
from categories.models import Category

PROJECTS_BOOLEAN_FIELDS = ['is_suggested']

PROJECTS_IMPORT_EXCLUDE_FIELDS = ['slug', 'date_created']


class ProjectResource(resources.ModelResource):

    categories = fields.Field(
        column_name='categories',
        attribute='categories',
        widget=ManyToManyWidget(Category, field='name')
    )

    class Meta:
        model = Project
        import_id_fields = ('slug',)
        export_order = ('name', 'description', 'categories')

    def get_import_fields(self):
        return [field for field in self.get_fields() if field.column_name not in PROJECTS_IMPORT_EXCLUDE_FIELDS]  # noqa

    def before_import_row(self, row, **kwargs):

        # remove keys
        for key in PROJECTS_IMPORT_EXCLUDE_FIELDS:
            if key in row:
                del row[key]
        # add/set keys
        row['is_suggested'] = False
        row['status'] = "published"

    def export_field(self, field, obj):
        """override export_field() to translate field values."""
        field_name = self.get_field_name(field)
        method = getattr(self, 'dehydrate_%s' % field_name, None)
        if method is not None:
            return method(obj)

        field_model = Project._meta.get_field(field.column_name)
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