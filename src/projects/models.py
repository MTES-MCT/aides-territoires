from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from aids.models import Aid


class Project(models.Model):

    name = models.CharField(
        _('Project name'),
        max_length=256,
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
    beneficiary = models.ManyToManyField(
        'accounts.User',
        verbose_name='Utilisateurs',
        related_name='projects',
        blank=True)

    due_date = models.DateTimeField(
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
        return reverse('project_detail_view', args=[self.slug])

    @property
    def id_slug(self):
        return '{}-{}'.format(self.id, self.slug)

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
