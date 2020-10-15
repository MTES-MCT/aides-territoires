from django.db import models
from django.db.models.expressions import RawSQL
from django.utils.translation import ugettext_lazy as _


class BackerQuerySet(models.QuerySet):

    def annotate_aids_count(self, related_fields, annotation_name):
        """Annotate the queryset with the number of related aids.

        We have to use a custom raw sql method because it's impossible to
        `annotate` the same query several times.

        See this bug:
        https://code.djangoproject.com/ticket/10060#comment:67
        """
        raw_sql = '''
            SELECT COUNT(*)
            FROM {model} as model
            WHERE model.backer_id = backers_backer.id
        '''.format(model=related_fields.through._meta.db_table)
        annotation = {annotation_name: RawSQL(raw_sql, [])}
        return self.annotate(**annotation)


class Backer(models.Model):
    """Represents an entity that backs aids."""

    objects = BackerQuerySet.as_manager()

    name = models.CharField(
        _('Name'),
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        _('Slug'),
        help_text=_(
            'Slug field is set when creating the backer '
            'and can not be changed after.'))
    is_corporate = models.BooleanField(
        _('Is a corporate backer?'),
        default=False)

    class Meta:
        verbose_name = _('Backer')
        verbose_name_plural = _('Backers')

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return '{}-{}'.format(self.id, self.slug)
