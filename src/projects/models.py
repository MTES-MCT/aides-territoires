from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from model_utils import Choices
from django_xworkflows import models as xwf_models


class ProjectWorkflow(xwf_models.Workflow):
    """Defines statuses for Projects."""

    log_model = ''

    states = Choices(
        ('draft', 'Brouillon'),
        ('reviewable', 'En revue'),
        ('published', 'Publié'),
    )
    initial_state = 'reviewable'
    transitions = (
        ('submit', 'draft', 'reviewable'),
        ('publish', 'reviewable', 'published'),
        ('unpublish', ('reviewable', 'published'), 'draft'),
    )


class Project(xwf_models.WorkflowEnabled, models.Model):

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
    categories = models.ManyToManyField(
        'categories.Category',
        verbose_name=_('Categories'),
        related_name='projects',
        blank=True)
    key_words = models.TextField(
        _('Key words'),
        help_text=_('key words associated to the project'),
        default='', blank=True)

    is_suggested = models.BooleanField(
        _('Is a suggested project?'),
        default=False,
        help_text=_(
            'If the project is suggested by a user'))

    status = xwf_models.StateField(
        ProjectWorkflow,
        verbose_name=_('Status'))
    date_created = models.DateTimeField(
        _('Date created'),
        default=timezone.now)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name

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

    def is_draft(self):
        return self.status == ProjectWorkflow.states.draft

    def is_under_review(self):
        return self.status == ProjectWorkflow.states.reviewable

    def is_published(self):
        return self.status == ProjectWorkflow.states.published
