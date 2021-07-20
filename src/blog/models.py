from os.path import splitext

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from model_utils import Choices
from django_xworkflows import models as xwf_models


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = 'blog/{}_logo{}'.format(name, extension)
    return filename


class BlogPostWorkflow(xwf_models.Workflow):
    """Defines statuses for Posts."""

    log_model = ''

    states = Choices(
        ('draft', 'Brouillon'),
        ('reviewable', 'En revue'),
        ('published', 'Publié'),
        ('deleted', 'Supprimé'),
    )
    initial_state = 'draft'
    transitions = (
        ('submit', 'draft', 'reviewable'),
        ('publish', 'reviewable', 'published'),
        ('unpublish', ('reviewable', 'published'), 'draft'),
    )


class BlogPostQuerySet(models.QuerySet):

    def published(self):
        """Only returns published objects."""

        return self.filter(status=BlogPostWorkflow.states.published.name)


class BlogPost(xwf_models.WorkflowEnabled, models.Model):

    objects = BlogPostQuerySet.as_manager()

    title = models.CharField(
        'Titre',
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        "Fragment d'URL",
        help_text='Laisser vide pour autoremplir.',
        blank=True)
    short_text = models.TextField(
        "Texte d'introduction",
        help_text="Introduction concise (inférieure à 256 caractères).",
        max_length=256,
        null=True, blank=True)
    text = models.TextField(
        "Contenu",
        blank=False)
    logo = models.FileField(
        "Illustration",
        help_text='Évitez les fichiers trop lourds. Préférez les fichiers svg.',
        upload_to=logo_upload_to,
        null=True, blank=True)

    category = models.ForeignKey(
        'BlogPostCategory',
        verbose_name="Catégorie de l'article de blog",
        on_delete=models.PROTECT,
        related_name='categories',
        null=True, blank=True)

    status = xwf_models.StateField(
        BlogPostWorkflow,
        verbose_name='Statut')

    # SEO
    meta_title = models.CharField(
        _('Meta title'),
        max_length=180,
        blank=True, default='',
        help_text=_('This will be displayed in SERPs. '
                    'Keep it under 60 characters. '
                    'Leave empty and we will reuse the post\'s title.'))
    meta_description = models.TextField(
        _('Meta description'),
        blank=True, default='',
        max_length=256,
        help_text=_('This will be displayed in SERPs. '
                    'Keep it under 120 characters.'))

    date_created = models.DateTimeField(
        'Date de création',
        default=timezone.now)
    date_updated = models.DateTimeField(
        'Date de mise à jour',
        auto_now=True)
    date_published = models.DateTimeField(
        'Première date de publication',
        null=True, blank=True)

    class Meta:
        verbose_name = 'Article de blog'
        verbose_name_plural = 'Articles de blog'
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.title)[:50]

    def set_publication_date(self):
        if self.is_published() and self.date_published is None:
            self.date_published = timezone.now()

    def save(self, *args, **kwargs):
        self.set_slug()
        self.set_publication_date()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_detail_view', args=[self.slug])

    def is_draft(self):
        return self.status == BlogPostWorkflow.states.draft

    def is_published(self):
        return self.status == BlogPostWorkflow.states.published


class BlogPostCategory(models.Model):

    name = models.CharField(
        'Nom',
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        "Fragment d'URL",
        help_text='Laisser vide pour autoremplir.',
        unique=True)
    description = models.TextField(
        'Description',
        blank=False)

    date_created = models.DateTimeField(
        'Date de création',
        default=timezone.now)
    date_updated = models.DateTimeField(
        'Date de mise à jour',
        auto_now=True)

    class Meta:
        verbose_name = 'Catégorie des articles de blog'
        verbose_name_plural = 'Catégories des articles de blog'

    def __str__(self):
        return self.name

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.name)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_post_list_view', kwargs={'category': self.slug})


class PromotionPostWorkflow(xwf_models.Workflow):
    """Defines statuses for Promotion posts."""

    log_model = ''

    states = Choices(
        ('draft', 'Brouillon'),
        ('reviewable', 'En revue'),
        ('published', 'Publié'),
        ('deleted', 'Supprimé'),
    )
    initial_state = 'draft'
    transitions = (
        ('submit', 'draft', 'reviewable'),
        ('publish', 'reviewable', 'published'),
        ('unpublish', ('reviewable', 'published'), 'draft'),
    )


class PromotionPost(xwf_models.WorkflowEnabled, models.Model):

    title = models.CharField(
        'Titre',
        max_length=256,
        db_index=True)
    slug = models.SlugField(
        "Fragment d'URL",
        help_text='Laisser vide pour autoremplir.',
        blank=True)
    short_text = models.TextField(
        "Texte d'introduction",
        help_text="Introduction concise (inférieure à 256 caractères).",
        max_length=256,
        null=True, blank=True)

    button_link = models.URLField(
        'Lien du bouton',
        blank=False)
    button_title = models.CharField(
        'Titre du bouton',
        max_length=120,
        db_index=True)

    perimeter = models.ForeignKey(
        'geofr.Perimeter',
        verbose_name='Périmètre',
        on_delete=models.PROTECT,
        null=True, blank=True)
    categories = models.ManyToManyField(
        'categories.Category',
        verbose_name='Sous-thématiques',
        related_name='promotionsPost',
        blank=True)
    programs = models.ManyToManyField(
        'programs.Program',
        verbose_name='Programmes',
        related_name='promotionsPost',
        blank=True)
    backers = models.ManyToManyField(
        'backers.Backer',
        verbose_name="Porteurs d'aides",
        related_name='promotionsPost',
        blank=True)

    status = xwf_models.StateField(
        PromotionPostWorkflow,
        verbose_name='Statut')

    date_created = models.DateTimeField(
        'Date de création',
        default=timezone.now)
    date_updated = models.DateTimeField(
        'Date de mise à jour',
        auto_now=True)

    class Meta:
        verbose_name = 'Communication promotionnelle'
        verbose_name_plural = 'Communications promotionnelles'

    def __str__(self):
        return self.title

    def set_slug(self):
        """Set the object's slug if it is missing."""
        if not self.slug:
            self.slug = slugify(self.title)[:50]

    def save(self, *args, **kwargs):
        self.set_slug()
        return super().save(*args, **kwargs)
