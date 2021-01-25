from django.utils.translation import gettext_lazy as _

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from aids.models import Aid


AIDS_EXPORT_EXCLUDE_FIELDS = [
    'id',
    'financer_suggestion', 'instructor_suggestion', 'perimeter_suggestion',
    'contact_email', 'contact_phone', 'contact_detail',
    'import_uniqueid', 'import_share_licence', 'import_last_access',
    'search_vector', 'tags', '_tags_m2m',
    'is_amendment', 'amended_aid', 'amendment_author_name', 'amendment_author_email', 'amendment_author_org', 'amendment_comment',  # noqa
]


class AidResource(resources.ModelResource):
    """Resource for Import-export."""

    # custom widgets to ForeignKey/ManyToMany information instead of ids
    author = fields.Field(
        column_name='author',
        attribute='author',
        widget=ForeignKeyWidget('accounts.User', field='full_name')
    )
    categories = fields.Field(
        column_name='categories',
        attribute='categories',
        widget=ManyToManyWidget('categories.Category', field='name')
    )
    financers = fields.Field(
        column_name='financers',
        attribute='financers',
        widget=ManyToManyWidget('backers.Backer', field='name')
    )
    instructors = fields.Field(
        column_name='instructors',
        attribute='instructors',
        widget=ManyToManyWidget('backers.Backer', field='name')
    )
    perimeter = fields.Field(
        column_name='perimeter',
        attribute='perimeter',
        widget=ForeignKeyWidget('geofr.Perimeter', field='name')
    )
    programs = fields.Field(
        column_name='programs',
        attribute='programs',
        widget=ManyToManyWidget('programs.Program', field='name')
    )

    class Meta:
        model = Aid
        exclude = AIDS_EXPORT_EXCLUDE_FIELDS
        # adding custom widgets breaks the usual order
        export_order = [field.name for field in Aid._meta.fields if field.name not in AIDS_EXPORT_EXCLUDE_FIELDS]  # noqa

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
