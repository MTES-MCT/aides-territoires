from os.path import splitext

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.db.models import Count, Case, When, IntegerField
from django.http import QueryDict
from django.urls import reverse
from django.utils import timezone

from aids.constants import AUDIENCES_GROUPED
from aids.models import Aid

from core.fields import ChoiceArrayField
from pages.models import Page


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = "minisites/{}_logo{}".format(name, extension)
    return filename


def meta_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.slug
    filename = "minisites/{}_meta{}".format(name, extension)
    return filename


class SearchPageQuerySet(models.QuerySet):
    """Custom queryset with additional filtering methods for search pages."""

    def has_administrators(self):
        """Only return search pages with an administrator."""

        return self.filter(administrator__isnull=False)

    def for_user(self, user):
        """Only return search pages which the user is the administrator."""
        qs = self.all()
        if not user.is_superuser:
            qs = qs.filter(administrator=user)
        return qs


class SearchPage(models.Model):
    """A single search result page with additional data.

    A customized search page is a pre-filtered search page with its own URL,
    configurable titles, descriptions, etc. and built for navigation and
    seo purpose.
    """

    objects = SearchPageQuerySet.as_manager()

    title = models.CharField("Titre", max_length=180, help_text="Le titre principal.")
    short_title = models.CharField(
        "Titre court",
        max_length=180,
        blank=True,
        default="",
        help_text="Un titre plus concis, pour affichage spécifique",
    )
    slug = models.SlugField(
        "Fragment d’URL",
        max_length=33,
        help_text="""Cette partie est utilisée dans l’URL.
             NE PAS CHANGER pour une page.
            DOIT être en minuscule pour les sites partenaires.
            Longueur max :33 caractères, mais si possible ne pas dépasser 23.""",
    )
    # The full domain name can not be longer than 64 characters for LetsEncrypt to be
    # able to generate a certificate.
    # We have a rather lengthy domain name, which leaves us with 33 characters
    # for the slug in production, and only 23 in staging.

    subdomain_enabled = models.BooleanField(
        "Afficher depuis un sous-domaine ?",
        default=True,
    )
    content = models.TextField(
        "Contenu de la page",
        help_text="Description complète de la page. Sera affichée au dessus des résultats.",
    )
    more_content = models.TextField(
        "Contenu additionnel",
        blank=True,
        help_text="Contenu révélé au clic sur le bouton « Voir plus ».",
    )
    tab_title = models.CharField(
        "Titre de l’onglet principal", blank=True, default="Accueil", max_length=180
    )
    contact_link = models.CharField(
        "URL du lien contact",
        help_text="""URL ou adresse email qui sera utilisé
        pour le lien « contact » dans le footer.""",
        blank=False,
        default="https://aides-territoires.beta.gouv.fr/contact/",
        max_length=300,
    )

    search_querystring = models.TextField(
        "Querystring", help_text="Les paramètres de recherche en format URL"
    )

    administrator = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        verbose_name="Administrateur",
        related_name="search_pages",
        null=True,
        blank=True,
    )

    highlighted_aids = models.ManyToManyField(
        "aids.Aid",
        verbose_name="Aides à mettre en avant",
        related_name="highlighted_in_search_pages",
        help_text="Il est possible de mettre jusqu’à 9 aides en avant. \
             Les aides mises en avant s’affichent en haut des résultats du portail, \
             et n’ont pas de mise en forme particulière.",
        blank=True,
    )
    excluded_aids = models.ManyToManyField(
        "aids.Aid",
        verbose_name="Aides à exclure",
        related_name="excluded_from_search_pages",
        blank=True,
    )

    # SEO
    meta_title = models.CharField(
        "Titre (balise meta)",
        max_length=180,
        blank=True,
        default="",
        help_text="Le titre qui sera affiché dans les SERPs.\
            Il est recommandé de le garder < \
            60 caractères. Laissez vide pour réutiliser le titre de la page.",
    )
    meta_description = models.TextField(
        "Description (balise meta)",
        blank=True,
        default="",
        max_length=256,
        help_text="Sera affichée dans les SERPs. À garder < 120 caractères.",
    )
    meta_image = models.FileField(
        "Image (balise meta)",
        null=True,
        blank=True,
        upload_to=meta_upload_to,
        help_text="Vérifiez que l’image a une largeur minimale de 1024px",
    )

    # custom_colors
    color_1 = models.CharField(
        "Couleur 1", max_length=10, blank=True, help_text="Couleur du fond principal"
    )
    color_2 = models.CharField(
        "Couleur 2",
        max_length=10,
        blank=True,
        help_text="Couleur du formulaire de recherche",
    )
    color_3 = models.CharField(
        "Couleur 3",
        max_length=10,
        blank=True,
        help_text="Couleur des boutons et bordures de titres",
    )
    color_4 = models.CharField(
        "Couleur 4", max_length=10, blank=True, help_text="Couleur des liens"
    )
    color_5 = models.CharField(
        "Couleur 5",
        max_length=10,
        blank=True,
        help_text="Couleur de fond du pied de page",
    )
    logo = models.FileField(
        "Logo",
        null=True,
        blank=True,
        upload_to=logo_upload_to,
        help_text="Évitez les fichiers trop lourds. Préférez les fichiers svg.",
    )
    logo_link = models.URLField(
        "Lien du logo",
        null=True,
        blank=True,
        help_text="L’URL vers laquelle renvoie un clic sur le logo partenaire",
    )

    # Search form customization fields
    show_categories_field = models.BooleanField(
        "Montrer le champ « thématiques » ?", default=True
    )
    available_categories = models.ManyToManyField(
        "categories.Category",
        verbose_name="Sous-thématiques",
        related_name="search_pages",
        blank=True,
    )

    show_audience_field = models.BooleanField(
        "Montrer le champ « structure » ?", default=True
    )
    available_audiences = ChoiceArrayField(
        verbose_name="Bénéficiaires de l’aide",
        null=True,
        blank=True,
        base_field=models.CharField(max_length=32, choices=AUDIENCES_GROUPED),
    )

    show_perimeter_field = models.BooleanField(
        "Montrer le champ « territoire » ?", default=True
    )
    show_backers_field = models.BooleanField(
        "Montrer le champ « porteur » ?", default=False
    )
    show_mobilization_step_field = models.BooleanField(
        "Montrer le champ « avancement du projet » ?", default=False
    )
    show_text_field = models.BooleanField(
        "Montrer le champ « recherche textuelle » ?", default=False
    )
    show_aid_type_field = models.BooleanField(
        "Montrer le champ « nature de l’aide » ?", default=False
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "page personnalisée"
        verbose_name_plural = "pages personnalisées"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("search_page", args=[self.slug])

    def get_base_querystring_data(self):
        # Sometime, the admin person enters a prefix "?" character
        # and we don't want it here.
        querystring = self.search_querystring.strip("?")
        data = QueryDict(querystring)
        return data

    def get_base_queryset(self, all_aids=False):
        """Return the list of aids based on the initial search querysting."""

        from aids.forms import AidSearchForm

        data = self.get_base_querystring_data()
        form = AidSearchForm(data)
        if all_aids:
            qs = form.filter_queryset(
                qs=Aid.objects.all(), apply_generic_aid_filter=False
            ).distinct()
        else:
            qs = form.filter_queryset(apply_generic_aid_filter=False).distinct()

        # Annotate aids contained in the highlighted_aids field
        # This field will be helpful to order the queryset
        # source: https://stackoverflow.com/a/44048355
        highlighted_aids_id_list = self.highlighted_aids.values_list(
            "id", flat=True
        )  # noqa
        qs = qs.annotate(
            is_highlighted_aid=Count(
                Case(
                    When(id__in=highlighted_aids_id_list, then=1),
                    output_field=IntegerField(),
                )
            )
        )
        # Simpler approach, but error-prone (aid could be highlighted in another SearchPage)  # noqa
        # qs = qs.annotate(is_highlighted_aid=Count('highlighted_in_search_pages'))  # noqa

        # Also exlude aids contained in the excluded_aids field
        excluded_aids_id_list = self.excluded_aids.values_list("id", flat=True)
        qs = qs.exclude(id__in=excluded_aids_id_list)

        return qs

    def get_aids_per_status(self):
        all_aids_per_status = (
            self.get_base_queryset(all_aids=True)
            .values("status")
            .annotate(count=Count("id", distinct=True))
        )
        return {s["status"]: s["count"] for s in list(all_aids_per_status)}

    def contact_link_is_email(self):
        try:
            validate_email(self.contact_link)
        except ValidationError:
            return False
        else:
            return True

    def delete(self):
        """
        Changes the source for alerts using that search page, so that
        they are now sent with the default AT as a source
        """

        # Avoid circular import
        Alert = apps.get_model("alerts", "Alert")

        alerts = Alert.objects.filter(source=self.slug)
        if alerts:
            alerts.update(source="aides-territoires")

        super(SearchPage, self).delete()


class SearchPageLite(SearchPage):
    """This proxy model is used for restricted/lite access,
    for instance when we want to give access to site users that
    are not super admin"""

    class Meta:
        proxy = True
        verbose_name = "page personnalisée"
        verbose_name_plural = "pages personnalisées"


class MinisiteTab(Page):
    """
    Proxy class to make Page model available for minisites
    as a Tab.
    """

    class Meta:
        proxy = True
        verbose_name = "onglet"
        verbose_name_plural = "onglets"


class MinisiteTabLite(Page):
    """
    Proxy class to make a lite admin for ministe Tab.
    """

    class Meta:
        proxy = True
        verbose_name = "onglet"
        verbose_name_plural = "onglets"
