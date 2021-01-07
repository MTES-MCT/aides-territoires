from os.path import splitext

from django.db import models
from django.db.models.expressions import RawSQL
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from aids.models import AidWorkflow


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = 'backers/{}_logo{}'.format(name, extension)
    return filename


class BackerGroup(models.Model):
    """Represents a group of backers."""

    name = models.CharField(
        _('Name'),
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        _('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)

    class Meta:
        verbose_name = _('Backer Group')
        verbose_name_plural = _('Backer Groups')

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return '{}-{}'.format(self.id, self.slug)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)


class BackerQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for backers."""

    def has_financed_aids(self):
        """Only return backers with financed_aids."""

        return self.exclude(financed_aids=None)

    def has_published_financed_aids(self):
        """Only return backers with published financed_aids."""

        qs = self.filter(financed_aids__status=AidWorkflow.states.published) \
            .distinct()
        return qs

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
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)
    is_corporate = models.BooleanField(
        _('Is a corporate backer?'),
        default=False)
    is_spotlighted = models.BooleanField(
        _('Is a spotlighted backer?'),
        default=False,
        help_text=_(
            'If the backer is spotlighted, its logo appears in the HomePage'))
    logo = models.FileField(
        _('Logo image'),
        null=True, blank=True,
        upload_to=logo_upload_to,
        help_text=_('Make sure the file is not too heavy. Prefer svg files.'))
    external_link = models.URLField(
        _('External link'),
        null=True, blank=True,
        help_text=_('The url for the backer\'s website'))
    description = models.TextField(
        _('Full description of the backer'),
        default='', blank=False)
    group = models.ForeignKey(
        'BackerGroup',
        verbose_name=_('Backer Group'),
        related_name='backers',
        on_delete=models.SET_NULL,
        null=True, blank=True)

    class Meta:
        verbose_name = _('Backer')
        verbose_name_plural = _('Backers')

    def __str__(self):
        return self.name

    @property
    def id_slug(self):
        return '{}-{}'.format(self.pk, self.slug)

    def get_absolute_url(self):
        url_args = [self.pk]
        if self.slug:
            url_args.append(self.slug)
        return reverse('backer_detail_view', args=url_args)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
