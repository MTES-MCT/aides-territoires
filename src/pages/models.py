from django.db import models
from django.utils import timezone
from django.contrib.flatpages.models import FlatPage


class PageQueryset(models.QuerySet):
    def at_pages(self, for_user=None):
        """Pages belonging to Aides-territoires main site."""

        qs = self.filter(minisite__isnull=True)
        if for_user and not for_user.is_superuser:
            # When listing pages for a given user, no pages
            # should be listed for a non-superuser
            qs = qs.none()
        return qs

    def minisite_tabs(self, for_user=None):
        """Pages that act as tabs for minisites."""

        qs = self.filter(minisite__isnull=False)
        if for_user and not for_user.is_superuser:
            # When listing pages for a given user, only pages
            # belonging the that user should be listed.
            qs = qs.filter(minisite__in=for_user.search_pages.all())
        return qs


class Page(FlatPage):
    """A static page that can be created/customized in admin."""

    objects = PageQueryset.as_manager()

    meta_title = models.CharField(
        "Titre (balise meta)",
        max_length=180,
        blank=True,
        default="",
        help_text="""Le titre qui sera affiché dans les SERPs.
        Il est recommandé de le garder < 60 caractères. Laissez vide pour
        réutiliser le titre de la page.""",
    )
    meta_description = models.TextField(
        "Description (balise meta)",
        blank=True,
        default="",
        max_length=256,
        help_text="""Le titre qui sera affiché dans les SERPs.
        Il est recommandé de le garder < 120 caractères.""",
    )

    minisite = models.ForeignKey(
        "search.SearchPage",
        verbose_name="Minisite",
        related_name="pages",
        help_text="Optionnel, lie cette page à un minisite.",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)


class Tab(models.Model):
    """A tab that can be created/customized in admin."""

    objects = PageQueryset.as_manager()

    title = models.CharField(
        "Titre",
        max_length=180,
        null=False,
        blank=False,
    )

    content = models.TextField("Contenu de l’onglet", blank=False)

    program = models.ForeignKey(
        "programs.Program",
        verbose_name="Program",
        related_name="pages",
        help_text="Programme lié à cette page.",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)


class FaqCategory(models.Model):
    name = models.CharField(
        "Nom",
        max_length=600,
        null=False,
        blank=False,
    )

    order = models.PositiveIntegerField("Rang", blank=False, default=1)

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Rubrique de la FAQ"
        verbose_name_plural = "Rubriques de la FAQ"
        ordering = ["order", "pk"]

    def __str__(self):
        return self.name


class FaqQuestionAnswer(models.Model):
    question = models.CharField(
        "Question",
        max_length=600,
        null=False,
        blank=False,
    )

    answer = models.TextField("Réponse", blank=False)

    faq_category = models.ForeignKey(
        "pages.FaqCategory",
        verbose_name="Rubrique",
        related_name="faqquestionanswer",
        help_text="Rubrique liée à cette Question-Réponse",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    program = models.ForeignKey(
        "programs.Program",
        verbose_name="Programme",
        related_name="faqquestionanswer",
        help_text="Programme lié à cette Question-Réponse",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    order = models.PositiveIntegerField("Rang", blank=False, default=1)

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Question-Réponse de la FAQ"
        verbose_name_plural = "Question-Réponse de la FAQ"
        ordering = ["faq_category", "order", "pk"]

    def __str__(self):
        return self.question
