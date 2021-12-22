from uuid import uuid4
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Project(models.Model):

    name = models.CharField(
        _('Project name'),
        max_length=256,
        null=False, blank=False,
        db_index=True)
    slug = models.SlugField(
        _('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
        blank=True)
    description = models.TextField(
        _('Full description of the project'),
        default='', blank=True)
    key_words = models.TextField(
        _('Key words'),
        help_text=_('key words associated to the project'),
        default='', blank=True)
    organizations = models.ManyToManyField(
        'organizations.Organization',
        verbose_name='Structures',
        blank=True)
    author = models.ManyToManyField(
        'accounts.User',
        verbose_name="Auteur",
        blank=True)

    due_date = models.DateField(
        "Date d'échéance",
        null=True, blank=True)

    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url_args = [self.id]
        if self.slug:
            url_args.append(self.slug)
        return reverse('project_detail_view', args=url_args)

    @property
    def id_slug(self):
        return '{}-{}'.format(self.id, self.slug)

    def set_slug(self):
        """Set the object's slug.

        Lots of aids have duplicate name, so we prefix the slug with random
        characters."""
        if not self.id:
            full_title = '{}-{}'.format(str(uuid4())[:4], self.name)
            self.slug = slugify(full_title)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
