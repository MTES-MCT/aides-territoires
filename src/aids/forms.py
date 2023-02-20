import re

from django import forms
from django.db.models import Q, F
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.postgres.search import SearchRank
from model_utils import Choices
from django.utils import timezone

from dsfr.forms import DsfrBaseForm
from core.forms import (
    AutocompleteModelChoiceField,
    AutocompleteSynonymChoiceField,
    AutocompleteModelMultipleChoiceField,
    MultipleChoiceFilterWidget,
    RichTextField,
)
from core.forms.baseform import AidesTerrBaseForm
from core.utils import remove_accents, parse_query
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters
from backers.models import Backer
from categories.fields import CategoryMultipleChoiceField
from categories.models import Category, Theme
from organizations.constants import ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES
from programs.models import Program
from projects.models import Project
from keywords.models import SynonymList
from aids.models import Aid, AidWorkflow, SuggestedAidProject, AidProject
from aids.constants import (
    AUDIENCES_GROUPED,
    FINANCIAL_AIDS_LIST,
    ALL_FINANCIAL_AIDS,
    TECHNICAL_AIDS,
    TECHNICAL_AIDS_LIST,
    AID_TYPES_GROUPED,
)
from aids.utils import filter_generic_aids


IS_CALL_FOR_PROJECT = ((None, "----"), (True, "Oui"), (False, "Non"))


class BaseAidForm(forms.ModelForm, DsfrBaseForm):
    """Base for all aid edition forms (front, admin).

    AidesTerrBaseForm isn't used here because it interferes with saving drafts.
    """

    short_title = forms.CharField(
        label="Titre du programme",
        required=False,
        max_length=64,
        widget=forms.TextInput(
            attrs={"placeholder": "Ex : Appel à projet innovation continue"}
        ),
    )
    description = RichTextField(
        label="Description complète de l’aide et de ses objectifs",
        widget=forms.Textarea(
            attrs={
                "placeholder": """
                Si vous avez un descriptif, n’hésitez pas à le copier ici.
                Essayez de compléter le descriptif avec le maximum d’informations.
                Si l’on vous contacte régulièrement pour vous demander les mêmes "
                informations, essayez de donner des éléments de réponses dans cet espace."
                """
            }
        ),
    )
    project_examples = RichTextField(
        label="Exemples d’applications ou de projets réalisés grâce à cette aide",
        required=False,
        help_text="Afin d’aider les territoires à mieux comprendre votre aide, donnez ici quelques exemples concrets de projets réalisables ou réalisés.",  # noqa
        widget=forms.Textarea(
            attrs={
                "placeholder": "Médiathèque, skatepark, accompagner des enfants en classe de neige, financer une usine de traitement des déchets, etc."  # noqa
            }
        ),
    )
    eligibility = RichTextField(label="Conditions d’éligibilité", required=False)
    contact = RichTextField(
        label="Contact pour candidater",
        required=True,
        help_text="N’hésitez pas à ajouter plusieurs contacts",
        widget=forms.Textarea(
            attrs={"placeholder": "Nom, prénom, e-mail, téléphone, commentaires…"}
        ),
    )
    local_characteristics = RichTextField(
        label="Spécificités locales",
        required=False,
        help_text="Décrivez les spécificités de cette aide locale.",
    )
    is_call_for_project = forms.BooleanField(
        label="Appel à projet / Manifestation d’intérêt", required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "aid_types" in self.fields:
            self.fields["aid_types"].choices = AID_TYPES_GROUPED

        if "targeted_audiences" in self.fields:
            self.fields["targeted_audiences"].choices = AUDIENCES_GROUPED

        if "recurrence" in self.fields:
            self.fields["recurrence"].required = True

        custom_labels = {
            "name": "Nom de l’aide",
            "financers": "Porteur de l’aide",
            "instructors": "Instructeur de l’aide",
            "new_backer": "…ou ajoutez un nouveau porteur d’aide",
            "destinations": "Types de dépenses / actions couvertes",
            "origin_url": "Plus d’informations",
            "application_url": "Candidater à l’aide",
            "is_call_for_project": "Cochez cette case s’il s’agit d’un appel à projets (AAP) ou d’un appel à manifestation d’intérêt (AMI)",  # noqa
        }
        for field, label in custom_labels.items():
            if field in self.fields:
                self.fields[field].label = label

        custom_help_text = {
            "new_backer": "Si le porteur de l’aide n’est pas déjà présent dans la liste précédente, vous pouvez utiliser ce champ pour nous le communiquer.",  # noqa
        }
        for field, help_text in custom_help_text.items():
            if field in self.fields:
                self.fields[field].help_text = help_text

    def save(self, commit=True):
        """Saves the instance.

        We update the aid search_vector here, because this is the only place
        we gather all the necessary data (object + m2m related objects).
        """
        financers = self.cleaned_data.get("financers", None)
        instructors = self.cleaned_data.get("instructors", None)
        categories = self.cleaned_data.get("categories", None)
        keywords = self.cleaned_data.get("keywords", None)
        programs = self.cleaned_data.get("programs", None)
        self.instance.set_search_vector_unaccented(
            financers, instructors, categories, keywords, programs
        )
        self.instance.date_updated = timezone.now()
        return super().save(commit=commit)


class AidAdminForm(BaseAidForm):
    """Custom Aid edition admin form."""

    EUROPEAN_AIDS = Choices(
        ("sectorial", "Grands programmes thématiques (Commission européenne)"),
        ("organizational", "Fonds structurels (FEDER, FSE+...)"),
    )

    perimeter_suggestion = forms.CharField(
        label="Périmètre suggéré",
        max_length=256,
        required=False,
        help_text="Le contributeur suggère ce nouveau périmètre",
    )

    financer_suggestion = forms.CharField(
        label="Porteurs suggérés",
        max_length=256,
        required=False,
        help_text="Ce porteur a été suggéré. Créez le nouveau porteur et ajouter le en tant que porteur d’aides via le champ approprié.",  # noqa
    )
    instructor_suggestion = forms.CharField(
        label="Instructeurs suggérés",
        max_length=256,
        required=False,
        help_text="Cet instructeur a été suggéré. Créez le nouveau porteur et ajouter le en tant qu’instructeur via le champ approprié.",  # noqa
    )
    categories = CategoryMultipleChoiceField(
        label="Sous-thématiques",
        required=False,
        widget=FilteredSelectMultiple("Sous-thématiques", True),
    )

    european_aid = forms.ChoiceField(
        label="Aide européenne ?",
        help_text="* Les fonds structurels (FEDER, FSE+...) sont les aides gérées par les conseils régionaux.",  # noqa
        required=False,
        widget=forms.RadioSelect,
        choices=EUROPEAN_AIDS,
    )

    class Meta:
        widgets = {
            "name": forms.Textarea(attrs={"rows": 3}),
            "mobilization_steps": forms.CheckboxSelectMultiple,
            "targeted_audiences": forms.CheckboxSelectMultiple,
            "aid_types": forms.CheckboxSelectMultiple,
            "destinations": forms.CheckboxSelectMultiple,
            "european_aid": forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "start_date" in self.fields:
            self.fields["start_date"].required = False

    def clean(self):
        """Validation routine if status is published."""

        data = super().clean()

        # If the aid is saved as draft, don't perform any data validation
        if data["status"].state == AidWorkflow.states.published:

            if not data.get("name", None):
                msg = "Veuillez compléter le champ nom de l’aide"
                self.add_error(
                    "name",
                    ValidationError(msg, code="missing_name"),
                )

            if not data.get("slug", None):
                msg = "Veuillez compléter le champ fragment d’url"
                self.add_error(
                    "slug",
                    ValidationError(msg, code="missing_slug"),
                )

            if not data.get("targeted_audiences", None):
                msg = "Veuillez compléter le champ bénéficiaires de l’aide"
                self.add_error(
                    "targeted_audiences",
                    ValidationError(msg, code="missing_targeted_audiences"),
                )

            if not data.get("aid_types", None):
                msg = "Veuillez compléter le champ type d’aide"
                self.add_error(
                    "aid_types",
                    ValidationError(msg, code="missing_aid_types"),
                )

            if not data.get("description", None):
                msg = "Veuillez compléter le champ description"
                self.add_error(
                    "description",
                    ValidationError(msg, code="missing_description"),
                )

            if not data.get("categories", None):
                msg = "Veuillez compléter le champ thématiques"
                self.add_error(
                    "categories",
                    ValidationError(msg, code="missing_categories"),
                )

            if not data.get("mobilization_steps", None):
                msg = "Veuillez compléter le champ état d’avancement du projet"
                self.add_error(
                    "mobilization_steps",
                    ValidationError(msg, code="missing_mobilization_steps"),
                )

            if not data.get("perimeter", None):
                msg = "Veuillez renseigner une zone géographique."
                self.add_error(
                    "perimeter",
                    ValidationError(msg, code="missing_perimeter"),
                )

            if not data.get("recurrence", None):
                msg = "Veuillez renseigner une récurrence."
                self.add_error(
                    "recurrence",
                    ValidationError(msg, code="missing_recurrence"),
                )

            if "recurrence" in data and data["recurrence"]:
                recurrence = data["recurrence"]
                submission_deadline = data.get("submission_deadline", None)

                if recurrence != "ongoing" and not submission_deadline:
                    msg = "Sauf pour les aides permanentes, veuillez indiquer la date de clôture de l’aide."  # noqa
                    self.add_error(
                        "submission_deadline",
                        ValidationError(msg, code="missing_submission_deadline"),
                    )

            if not self.data.get("aidfinancer_set-0-backer"):
                raise ValidationError("Merci d’indiquer un porteur d’aide.")

            return data
        else:
            return data


class AidEditForm(BaseAidForm):

    programs = forms.ModelMultipleChoiceField(
        label="Programme d’aides", queryset=Program.objects.all(), required=False
    )
    financers = AutocompleteModelMultipleChoiceField(
        label="Porteurs d’aides",
        queryset=Backer.objects.all(),
        required=False,
        help_text="Saisissez quelques caractères et sélectionnez une valeur parmi les suggestions.",
    )
    financer_suggestion = forms.CharField(
        label="Suggérer un nouveau porteur",
        max_length=256,
        required=False,
        help_text="Suggérez un porteur si vous ne trouvez pas votre choix dans la liste principale.",  # noqa
    )
    instructors = AutocompleteModelMultipleChoiceField(
        label="Instructeurs",
        queryset=Backer.objects.all(),
        required=False,
        help_text="Saisissez quelques caractères et sélectionnez une valeur parmi les suggestions.",
    )
    instructor_suggestion = forms.CharField(
        label="Suggérer un nouvel instructeur",
        max_length=256,
        required=False,
        help_text="Suggérez un instructeur si vous ne trouvez pas votre choix dans la liste principale.",  # noqa
    )

    perimeter = AutocompleteModelChoiceField(
        queryset=Perimeter.objects.all(),
        label="Zone géographique couverte par l’aide",
        help_text="""
            La zone géographique sur laquelle l’aide est disponible.<br />
            Exemples de zones valides :
            <ul>
            <li>France</li>
            <li>Bretagne (Région)</li>
            <li>Métropole du Grand Paris (EPCI)</li>
            <li>Outre-mer</li>
            <li>Wallis et Futuna</li>
            <li>Massif Central</li>
            </ul>
        """,
    )
    perimeter_suggestion = forms.CharField(
        label="Vous ne trouvez pas de zone géographique appropriée ?",
        max_length=256,
        required=False,
        help_text="""
            Si vous ne trouvez pas de zone géographique suffisamment précise dans la
            liste existante, spécifiez « France » et décrivez brièvement ici le
            périmètre souhaité.
        """,
    )
    categories = CategoryMultipleChoiceField(
        label="Thématiques de l’aide",
        required=False,
        help_text="Sélectionnez la ou les thématiques associées à votre aide. N’hésitez pas à en choisir plusieurs.",  # noqa
    )
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    origin_url = forms.URLField(
        label="Lien vers plus d’information (url d’origine, site du porteur d’aides)",
        required=True,
        max_length=500,
    )

    application_url = forms.URLField(
        label="Lien vers une démarche en ligne pour candidater",
        required=False,
        max_length=500,
    )

    class Meta:
        model = Aid
        fields = [
            "name",
            "name_initial",
            "slug",
            "short_title",
            "description",
            "categories",
            "project_examples",
            "targeted_audiences",
            "financers",
            "financer_suggestion",
            "instructors",
            "instructor_suggestion",
            "in_france_relance",
            "recurrence",
            "start_date",
            "predeposit_date",
            "submission_deadline",
            "perimeter",
            "perimeter_suggestion",
            "is_call_for_project",
            "programs",
            "aid_types",
            "subvention_rate",
            "subvention_comment",
            "loan_amount",
            "recoverable_advance_amount",
            "other_financial_aid_comment",
            "is_charged",
            "mobilization_steps",
            "destinations",
            "eligibility",
            "origin_url",
            "application_url",
            "contact",
            "local_characteristics",
        ]
        widgets = {
            "mobilization_steps": MultipleChoiceFilterWidget,
            "destinations": MultipleChoiceFilterWidget,
            "targeted_audiences": MultipleChoiceFilterWidget,
            "aid_types": MultipleChoiceFilterWidget,
            "start_date": forms.TextInput(
                attrs={"type": "date", "placeholder": "jj/mm/aaaa"}
            ),
            "predeposit_date": forms.TextInput(
                attrs={"type": "date", "placeholder": "jj/mm/aaaa"}
            ),
            "submission_deadline": forms.TextInput(
                attrs={"type": "date", "placeholder": "jj/mm/aaaa"}
            ),
        }

    def __init__(self, *args, **kwargs):

        # The form validation rule will change depending on the
        # new aid status.
        self.requested_status = kwargs.pop("requested_status", None)

        super().__init__(*args, **kwargs)

        if self.requested_status is None:
            self.requested_status = self.instance.status

        if "subvention_rate" in self.fields:
            range_widgets = self.fields["subvention_rate"].widget.widgets
            range_widgets[0].attrs["placeholder"] = "Taux de subvention min."
            range_widgets[1].attrs["placeholder"] = "Taux de subvention max."

        if "mobilization_steps" in self.fields:
            self.fields["mobilization_steps"].required = True

        if "targeted_audiences" in self.fields:
            self.fields["targeted_audiences"].required = True

        if "aid_types" in self.fields:
            self.fields["aid_types"].required = True

        if "categories" in self.fields:
            self.fields["categories"].required = True

    def full_clean(self):
        if self.requested_status == "draft":
            for field_name in self.fields.keys():
                if field_name == "name":
                    continue
                self.fields[field_name].required = False

        return super().full_clean()

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        # If the aid is saved as draft, don't perform any data validation
        if self.requested_status == "draft":
            return data

        if "recurrence" in data and data["recurrence"]:
            recurrence = data["recurrence"]
            submission_deadline = data.get("submission_deadline", None)

            if recurrence != "ongoing" and not submission_deadline:
                msg = "Sauf pour les aides permanentes, veuillez indiquer la date limite de soumission."  # noqa
                self.add_error(
                    "submission_deadline",
                    ValidationError(msg, code="missing_submission_deadline"),
                )

        if "financers" in self.fields:
            if not any((data.get("financers"), data.get("financer_suggestion"))):
                msg = "Merci d’indiquer un porteur d’aide."
                self.add_error("financers", msg)

        return data


class BaseAidSearchForm(AidesTerrBaseForm):
    """Main form for search engine."""

    AID_CATEGORY_CHOICES = (
        ("", ""),
        ("funding", "Financière"),
        ("non-funding", "Non-financière"),
    )

    ORDER_BY_CHOICES = (
        ("relevance", "Tri : pertinence"),
        ("publication_date", "Tri : date de publication (plus récentes en premier)"),
        ("submission_deadline", "Tri : date de clôture (plus proches en premier)"),
    )

    CATEGORIES_QS = Category.objects.select_related("theme").order_by(
        "theme__name", "name"
    )

    text = AutocompleteSynonymChoiceField(
        label="Mot-clés", queryset=SynonymList.objects.all(), required=False
    )

    apply_before = forms.DateField(
        label="Candidater avant…",
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    published_after = forms.DateTimeField(
        label="Publiée après…",
        required=False,
        widget=forms.TextInput(attrs={"type": "date"}),
    )
    aid_type = forms.MultipleChoiceField(
        label="Nature de l’aide",
        choices=AID_TYPES_GROUPED,
        required=False,
    )
    financial_aids = forms.MultipleChoiceField(
        label="Aides financières",
        required=False,
        choices=ALL_FINANCIAL_AIDS,
        widget=forms.CheckboxSelectMultiple,
    )
    technical_aids = forms.MultipleChoiceField(
        label="Aides en ingénierie",
        required=False,
        choices=TECHNICAL_AIDS,
        widget=forms.CheckboxSelectMultiple,
    )
    is_charged = forms.ChoiceField(
        label="Aides payantes ou gratuites",
        required=False,
        choices=Aid.IS_CHARGED,
    )
    mobilization_step = forms.MultipleChoiceField(
        label="Avancement du projet",
        required=False,
        choices=Aid.STEPS,
    )
    destinations = forms.MultipleChoiceField(
        label="Actions concernées",
        required=False,
        choices=Aid.DESTINATIONS,
    )
    recurrence = forms.ChoiceField(
        label="Récurrence", required=False, choices=Aid.RECURRENCES
    )
    call_for_projects_only = forms.BooleanField(
        label="Appels à projets / Appels à manifestation d’intérêt uniquement",
        required=False,
    )
    backers = AutocompleteModelMultipleChoiceField(
        label="Porteurs d’aides", queryset=Backer.objects.all(), required=False
    )
    programs = forms.ModelMultipleChoiceField(
        label="Programmes d’aides",
        queryset=Program.objects.all(),
        to_field_name="slug",
        required=False,
    )
    in_france_relance = forms.BooleanField(
        label="Aides France Relance :", required=False
    )
    themes = forms.ModelMultipleChoiceField(
        label="Thématiques",
        queryset=Theme.objects.all(),
        to_field_name="slug",
        required=False,
        widget=forms.MultipleHiddenInput,
    )
    categories = CategoryMultipleChoiceField(
        group_by_theme=True,
        label="Thématiques",  # Not a mistake
        queryset=CATEGORIES_QS,
        to_field_name="slug",
        required=False,
    )
    targeted_audiences = forms.MultipleChoiceField(
        label="La structure pour laquelle vous recherchez des aides est…",
        required=False,
        choices=ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    perimeter = AutocompleteModelChoiceField(
        queryset=Perimeter.objects.all(), label="Votre territoire", required=False
    )
    origin_url = forms.URLField(label="URL d’origine", required=False)

    # This field is not related to the search, but is submitted
    # in views embedded through an iframe.
    integration = forms.CharField(required=False, widget=forms.HiddenInput)

    # This field is used to sort results
    order_by = forms.ChoiceField(
        label="Trier par", required=False, choices=ORDER_BY_CHOICES
    )

    def clean_zipcode(self):
        zipcode = self.cleaned_data["zipcode"]
        if zipcode and re.match(r"\d{5}", zipcode) is None:
            msg = "Ce code postal semble invalide."
            raise forms.ValidationError(msg)

        return zipcode

    def filter_queryset(self, qs=None, apply_generic_aid_filter=True):  # noqa
        """Filter querysets depending of input data."""

        # If no qs was passed, just start with all published aids
        if qs is None:
            qs = Aid.objects.published().open()

        if not self.is_bound:
            return qs

        # Populate cleaned_data
        if not hasattr(self, "cleaned_data"):
            self.full_clean()

        perimeter = self.cleaned_data.get("perimeter", None)
        if perimeter:
            qs = self.perimeter_filter(qs, perimeter)

        mobilization_steps = self.cleaned_data.get("mobilization_step", None)
        if mobilization_steps:
            qs = qs.filter(mobilization_steps__overlap=mobilization_steps)

        # Those two form fields are split for form readability,
        # but they relate to a single model field.
        financial_aids = self.cleaned_data.get("financial_aids", [])
        technical_aids = self.cleaned_data.get("technical_aids", [])
        aid_types = financial_aids + technical_aids

        aid_type = self.cleaned_data.get("aid_type", [])
        if "financial_group" in aid_type:
            aid_types += FINANCIAL_AIDS_LIST
        if "technical_group" in aid_type:
            aid_types += TECHNICAL_AIDS_LIST

        if aid_type and not aid_types:
            aid_types = aid_type

        if aid_types:
            qs = qs.filter(aid_types__overlap=aid_types)

        destinations = self.cleaned_data.get("destinations", None)
        if destinations:
            qs = qs.filter(destinations__overlap=destinations)

        apply_before = self.cleaned_data.get("apply_before", None)
        if apply_before:
            qs = qs.filter(submission_deadline__lte=apply_before)

        published_after = self.cleaned_data.get("published_after", None)
        if published_after:
            qs = qs.filter(date_published__gte=published_after)

        recurrence = self.cleaned_data.get("recurrence", None)
        if recurrence:
            qs = qs.filter(recurrence=recurrence)

        call_for_projects_only = self.cleaned_data.get("call_for_projects_only", False)
        if call_for_projects_only:
            qs = qs.filter(is_call_for_project=True)

        is_charged = self.cleaned_data.get("is_charged", False)
        if is_charged == "False":
            qs = qs.filter(is_charged=False)
        elif is_charged == "True":
            qs = qs.filter(is_charged=True)

        in_france_relance = self.cleaned_data.get("in_france_relance", False)
        if in_france_relance:
            qs = qs.filter(in_france_relance=True)

        text = self.cleaned_data.get("text", None)
        if text:
            text_unaccented = remove_accents(text)
            query = parse_query(text_unaccented)
            qs = qs.filter(search_vector_unaccented=query).annotate(
                rank=SearchRank(F("search_vector_unaccented"), query)
            )

        targeted_audiences = self.cleaned_data.get("targeted_audiences", None)
        if targeted_audiences:
            qs = qs.filter(targeted_audiences__overlap=targeted_audiences)

        categories = self.cleaned_data.get("categories", None)
        if categories:
            qs = qs.filter(categories__in=categories)

        programs = self.cleaned_data.get("programs", None)
        if programs:
            qs = qs.filter(programs__in=programs)

        # We filter by theme only if no categories were provided.
        # This is to handle the following edge case: on the multi-step search
        # form, the user selects a theme, then on the last step, doesn't select
        # any categories and just click "Search".
        themes = self.cleaned_data.get("themes", None)
        if themes and not categories:
            qs = qs.filter(categories__theme__in=themes)

        backers = self.cleaned_data.get("backers", None)
        if backers:
            qs = qs.filter(Q(financers__in=backers) | Q(instructors__in=backers))

        origin_url = self.cleaned_data.get("origin_url", None)
        if origin_url:
            qs = qs.filter(origin_url=origin_url)

        if apply_generic_aid_filter:
            qs = self.generic_aid_filter(qs)

        return qs

    def get_order_fields(self, qs, has_highlighted_aids=False, pre_order=None):
        """On which fields must this queryset be sorted?."""

        # Default results order
        # show the narrower perimeter first, then aids with a deadline
        order_fields = ["perimeter__scale", "submission_deadline"]
        # If the search comes from a PP
        if pre_order and has_highlighted_aids and not self.cleaned_data.get("order_by"):
            if pre_order == "publication_date":
                order_fields = (
                    ["-is_highlighted_aid"] + ["-date_published"] + order_fields
                )
            elif pre_order == "submission_deadline":
                order_fields = (
                    ["-is_highlighted_aid"] + ["submission_deadline"] + order_fields
                )
            elif pre_order == "relevance":
                order_fields = ["-is_highlighted_aid"] + order_fields
        elif has_highlighted_aids and not self.cleaned_data.get("order_by"):
            order_fields = ["is_highlighted_aid"] + order_fields

        # If the user submitted a text query, we order by query rank first
        text = self.cleaned_data.get("text", None)
        if text:
            order_fields = ["-rank"] + order_fields

        # If the user requested a manual order by publication date
        if self.cleaned_data.get("order_by"):
            manual_order = self.cleaned_data.get("order_by", "relevance")
            if manual_order == "publication_date":
                order_fields = ["-date_published"] + order_fields
            elif manual_order == "submission_deadline":
                order_fields = ["submission_deadline"] + order_fields

        return order_fields

    def order_queryset(self, qs, has_highlighted_aids=False, pre_order=None):
        """Set the order value on the queryset."""
        qs = qs.order_by(
            *self.get_order_fields(
                qs,
                has_highlighted_aids=has_highlighted_aids,
                pre_order=pre_order,
            )
        )
        return qs

    def perimeter_filter(self, qs, search_perimeter):
        """Filter queryset depending on the given perimeter.

        When we search for a given perimeter, we must return all aids:
         - where the perimeter is wider and contains the searched perimeter ;
         - where the perimeter is smaller and contained by the search
         perimeter ;

        E.g if we search for aids in "Hérault (department), we must display all
        aids that are applicable to:

         - Hérault ;
         - Occitanie ;
         - France ;
         - Europe ;
         - M3M (and all other epcis in Hérault) ;
         - Montpellier (and all other communes in Hérault) ;
        """
        perimeter_ids = get_all_related_perimeters(search_perimeter.id, values=["id"])
        qs = qs.filter(perimeter__in=perimeter_ids)
        return qs

    def generic_aid_filter(self, qs):
        """
        We should never have both the generic aid and its local version
        together on search results.
        Which one should be removed from the result ? It depends...
        We consider the scale perimeter associated to the local aid.
        - When searching on a wider area than the local aid's perimeter,
          then we display the generic version.
        - When searching on a smaller area than the local aid's perimeter,
          then we display the local version.
        """
        search_perimeter = self.cleaned_data.get("perimeter", None)

        qs = filter_generic_aids(qs, search_perimeter)
        return qs


class AidSearchForm(BaseAidSearchForm):
    """The main search result filter form."""

    targeted_audiences = forms.MultipleChoiceField(
        label="Le bénéficiaire",
        required=False,
        choices=ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES,
    )


class AdvancedAidFilterForm(BaseAidSearchForm):
    """An "advanced" aid list filter form with more criterias."""

    targeted_audiences = forms.MultipleChoiceField(
        label="La structure pour laquelle vous recherchez des aides est…",
        required=False,
        choices=ORGANIZATION_TYPES_SINGULAR_ALL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )


class DraftListAidFilterForm(AidesTerrBaseForm):
    """allow the filtering of aids in the drafts list"""

    AID_STATE_CHOICES = [
        ("", "Sélectionnez une option"),
        ("open", "Ouverte"),
        ("deadline", "Expire bientôt"),
        ("expired", "Expirée"),
    ]

    AID_DISPLAY_STATUS_CHOICES = [
        ("", "Sélectionnez une option"),
        ("hidden", "Non affichée"),
        ("live", "Affichée"),
    ]

    state = forms.ChoiceField(
        label="Échéance", required=False, choices=AID_STATE_CHOICES
    )

    display_status = forms.ChoiceField(
        label="Affichage", required=False, choices=AID_DISPLAY_STATUS_CHOICES
    )


class AidMatchProjectForm(forms.ModelForm, AidesTerrBaseForm):
    """allow user to associate aid to existing projects."""

    projects = forms.ModelMultipleChoiceField(
        label="Projet à associer",
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Aid
        fields = ["projects"]


class AidProjectStatusForm(forms.ModelForm, AidesTerrBaseForm):
    class Meta:
        model = AidProject
        fields = ["aid_requested", "aid_obtained", "aid_paid", "aid_denied"]

    def clean(self):

        data = super().clean()
        if data.get("aid_obtained") and data.get("aid_denied"):
            msg = "L’aide ne peut être à la fois « obtenue » et « rejetée »"
            self.add_error("aid_denied", msg)
            self.add_error("aid_obtained", msg)
        elif data.get("aid_paid") and data.get("aid_denied"):
            msg = "L’aide ne peut être à la fois « versée » et « rejetée »"
            self.add_error("aid_denied", msg)
            self.add_error("aid_paid", msg)

        return data


class SuggestAidMatchProjectForm(AidesTerrBaseForm):
    """allow user to suggest an aid to an existing project."""

    project = forms.ModelMultipleChoiceField(
        queryset=Project.objects.filter(
            is_public=True, status=Project.STATUS.published
        ),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    aid = forms.CharField(
        label="URL de l’aide que vous souhaitez suggérer",
        required=True,
        help_text="Coller ici l’URL de l’aide que vous souhaitez suggérer pour le projet.",
    )

    def get_origin_page_from_post_data(self):

        origin_page = self.data.get("origin_page", None)
        return origin_page

    def clean_aid(self):
        aid_url = self.cleaned_data["aid"]
        projects = self.cleaned_data["project"]
        origin_page = self.get_origin_page_from_post_data()

        if self.data.get("aid"):
            try:
                if origin_page == "aid_detail_page":
                    aid = Aid.objects.get(slug=aid_url)
                else:
                    aid_slug = str(aid_url.partition("aides/")[2])
                    aid_slug = str(aid_slug.partition("/")[0])
                    aid = Aid.objects.get(slug=aid_slug)

                for project in projects:
                    if SuggestedAidProject.objects.filter(
                        aid=aid.pk, project=project.pk
                    ).exists():
                        msg = "Cette aide a déjà été suggérée pour ce projet."
                        self.add_error("aid", msg)
                        return aid_url
                    elif AidProject.objects.filter(
                        aid=aid.pk, project=project.pk
                    ).exists():
                        msg = "Cette aide est déjà associée à ce projet."
                        self.add_error("aid", msg)
                        return aid_url
                return aid
            except Exception:
                msg = "Cette url ne correspond pas à une aide actuellement publiée. \
                Merci de saisir une url correcte."
                self.add_error("aid", msg)
                return aid_url
