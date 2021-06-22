from django.utils.translation import gettext_lazy as _
from django.db.models.fields import TextField, CharField, URLField

from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE

from aids.models import Aid
from accounts.models import User
from categories.models import Category
from backers.models import Backer
from geofr.models import Perimeter
from programs.models import Program
from projects.models import Project


AIDS_BOOLEAN_FIELDS = ['is_call_for_project', 'in_france_relance',
                       'is_imported']  # is_amendment

AIDS_EXPORT_EXCLUDE_FIELDS = [
    'short_title',
    'financer_suggestion', 'instructor_suggestion', 'perimeter_suggestion',
    'contact_email', 'contact_phone', 'contact_detail',
    'import_uniqueid', 'import_share_licence', 'import_last_access',
    'search_vector',
    'is_amendment', 'amended_aid', 'amendment_author_name', 'amendment_author_email', 'amendment_author_org', 'amendment_comment',  # noqa
    'local_characteristics']
AIDS_IMPORT_EXCLUDE_FIELDS = [
    'slug', 'status', 'date_updated', 'date_published']
AIDS_IMPORT_CLEAN_FIELDS = [
    'is_imported', 'author', 'subvention_rate']

ADMIN_EMAIL = 'admin@test.com'


class AidResource(resources.ModelResource):
    """Resource for Import-export."""

    # custom widgets to ForeignKey/ManyToMany information instead of ids
    author = fields.Field(
        column_name='author',
        attribute='author',
        widget=ForeignKeyWidget(User, field='email')
    )
    categories = fields.Field(
        column_name='categories',
        attribute='categories',
        widget=ManyToManyWidget(Category, field='name')
    )
    financers = fields.Field(
        column_name='financers',
        attribute='financers',
        widget=ManyToManyWidget(Backer, field='name')
    )
    instructors = fields.Field(
        column_name='instructors',
        attribute='instructors',
        widget=ManyToManyWidget(Backer, field='name')
    )
    perimeter = fields.Field(
        column_name='perimeter',
        attribute='perimeter',
        widget=ForeignKeyWidget(Perimeter, field='name')
    )
    programs = fields.Field(
        column_name='programs',
        attribute='programs',
        widget=ManyToManyWidget(Program, field='name')
    )
    projects = fields.Field(
        column_name='projects',
        attribute='projects',
        widget=ManyToManyWidget(Project, field='name')
    )

    class Meta:
        model = Aid
        import_id_fields = ('id',)
        exclude = AIDS_EXPORT_EXCLUDE_FIELDS
        # adding custom widgets breaks the usual order
        export_order = [field.name for field in Aid._meta.fields if field.name not in AIDS_EXPORT_EXCLUDE_FIELDS]  # noqa

    def get_import_fields(self):
        return [field for field in self.get_fields() if field.column_name not in AIDS_IMPORT_EXCLUDE_FIELDS]  # noqa

    def get_user_visible_fields(self):
        return [field for field in self.get_fields() if field.column_name not in AIDS_IMPORT_EXCLUDE_FIELDS]  # noqa

    def before_import_row(self, row, **kwargs):
        """
        Why do we need to override before_import_row() ?
        - to revert the translation of row keys (header)
        - to clean/set some values
        """
        # rename keys
        for key in list(row.keys()):
            for field in (Aid._meta.model._meta.fields + Aid._meta.model._meta.many_to_many): # noqa
                if field.verbose_name == key:
                    row[field.name] = row[key]
                    del row[key]
        # remove keys
        for key in AIDS_IMPORT_EXCLUDE_FIELDS:
            if key in row:
                del row[key]
        # add/set keys
        if 'projects' not in row:
            row['author'] = row.get('author', ADMIN_EMAIL) or ADMIN_EMAIL
            row['is_imported'] = True
        if 'subvention_rate' in row:
            if row['subvention_rate']:
                row['subvention_rate'] = row['subvention_rate'] \
                    .replace('(', '[') \
                    .replace('None', '')

    def import_field(self, field, obj, data, is_m2m=False):
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
                data[field.column_name] = data.get(field.column_name, '') or ''
            # avoid empty string for fields with base_field
            if hasattr(field_model, 'base_field') and not data[field.column_name]:  # noqa
                data[field.column_name] = None
            # revert the translation of some specific fields
            if data[field.column_name]:
                # simple fields with choices
                if field_model.choices:
                    data[field.column_name] = next(k for k,v in iter(dict(field_model.flatchoices).items()) if v == data[field.column_name])  # noqa
                # ChoiceArrayField fields
                if hasattr(field_model, 'base_field') and field_model.base_field.choices:  # noqa
                    data[field.column_name] = [k for k,v in iter(dict(field_model.base_field.flatchoices).items()) if str(v) in data[field.column_name]]  # noqa
                    data[field.column_name] = ','.join(data[field.column_name])
                # BooleanField fields
                if field.column_name in AIDS_BOOLEAN_FIELDS:
                    if data[field.column_name] == _('Yes'):
                        data[field.column_name] = True
                    elif data[field.column_name] == _('No'):
                        data[field.column_name] = False
                    else:
                        data[field.column_name] = None
            field.save(obj, data, is_m2m)

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
        method = getattr(self, 'dehydrate_%s' % field_name, None)
        if method is not None:
            return method(obj)

        field_model = Aid._meta.get_field(field.column_name)
        if field_model.serialize:
            # simple fields with choices: use get_FOO_display to translate
            if field_model.choices:
                value = getattr(obj, f'get_{field.column_name}_display')()
                return field.widget.render(value, obj)
            # For Text and Char fields, we remove illegal characters
            elif isinstance(field_model, (TextField, CharField)):
                export_value = field.export(obj)
                export_value = ILLEGAL_CHARACTERS_RE.sub('', export_value)
                return export_value
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

        # subvention_rate
        if field.column_name == 'subvention_rate':
            if field.get_value(obj) is None:
                return ''
            else:
                lower = field.get_value(obj).lower or ''
                upper = field.get_value(obj).upper or ''
                return f'[{lower}, {upper})'
        return field.export(obj)
