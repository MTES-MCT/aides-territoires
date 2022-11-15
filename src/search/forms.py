from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from categories.fields import CategoryMultipleChoiceField, CategoryChoiceIterator
from core.forms.fields import RichTextField
from pages.admin import PageForm

AUDIENCES = [
    (
        "Une collectivité",
        (
            ("commune", "Commune"),
            ("epci", "Intercommunalité / Pays"),
            ("department", "Département"),
            ("region", "Région"),
            ("special", "Collectivité d'outre-mer à statuts particuliers"),
        ),
    ),
    (
        "Un autre bénéficiaire",
        (
            ("public_org", "Établissement public"),
            ("public_cies", "Entreprise publique locale (Sem, Spl, SemOp)"),
            ("association", "Association"),
            ("private_sector", "Entreprise privée"),
            ("private_person", "Particulier"),
            ("farmer", "Agriculteur"),
            ("researcher", "Recherche"),
        ),
    ),
]


class AudienceWidget(forms.widgets.ChoiceWidget):
    """Custom widget for the audience search step."""

    allow_multiple_selected = False


class CategoryIterator(CategoryChoiceIterator):
    def theme_label(self, theme_name):
        return theme_name


class CategoryChoiceField(forms.ModelMultipleChoiceField):

    iterator = CategoryIterator


class CategoryWidget(forms.widgets.ChoiceWidget):
    """Custom widget to select categories grouped by themes."""

    allow_multiple_selected = True
    template_name = "search/forms/widgets/category_widget.html"


class SearchPageAdminForm(forms.ModelForm):
    content = RichTextField(
        label="Contenu de la page",
        help_text="Description complète de la page. Sera affichée au dessus des résultats.",
    )
    more_content = RichTextField(
        label="Contenu additionnel",
        help_text="Contenu caché, révélé au clic sur le bouton « Voir plus ».",
    )
    available_categories = CategoryMultipleChoiceField(
        label="Sous-thématiques",
        required=False,
        widget=FilteredSelectMultiple("Sous-thématiques", True),
    )

    def clean(self):
        """Validate search page customization consistency.

        Filters consistency: we need to make sure that at least one
        search form field is selected.

        """
        data = super().clean()

        search_fields = [
            "show_perimeter_field",
            "show_audience_field",
            "show_categories_field",
            "show_mobilization_step_field",
            "show_aid_type_field",
            "show_backers_field",
            "show_text_field",
        ]

        # If there is no form customization fields, then we don't
        # need to run the fields validation. That's tipically the case
        # for lite admin page available to contributors that don't have
        # access to form customization.
        all_form_fields = self.fields.keys()
        has_form_customization_fields = any(
            field in all_form_fields for field in search_fields
        )
        if not has_form_customization_fields:
            return data

        nb_filters = 0
        for field in search_fields:
            if field in data and data[field]:
                nb_filters += 1

        if nb_filters == 0:
            raise ValidationError(
                "Vous devez sélectionner au moins un filtre pour le formulaire de recherche.",
                code="not_enough_filters",
            )

        if nb_filters > 3:
            raise ValidationError(
                "Vous ne devez pas sélectionner plus de trois filtres pour le formulaire de recherche.",  # noqa
                code="too_many_filters",
            )

        return data


class MinisiteTabForm(PageForm):
    pass


class MinisiteTabFormLite(MinisiteTabForm):
    url = forms.CharField(required=False)

    def build_url_from_title(self, title):
        slug = slugify(title)[:50]
        url = f"/{slug}/"
        return url

    def clean_url(self):
        url = self.cleaned_data["url"]
        if not url:
            title = self.cleaned_data.get("title")
            url = self.build_url_from_title(title)
        return url

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.url = self.cleaned_data["url"]
        return super().save(commit=commit)
