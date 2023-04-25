import requests
import json
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.postgres.search import SearchQuery, SearchHeadline
from django.db.models import Q, Count, Prefetch
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    FormView,
    RedirectView,
)
from django.views import View
from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied

from braces.views import MessageMixin

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin
from backers.models import Backer
from aids.forms import (
    AidEditForm,
    AidSearchForm,
    AdvancedAidFilterForm,
    DraftListAidFilterForm,
    AidMatchProjectForm,
    SuggestAidMatchProjectForm,
    AidProjectStatusForm,
)
from aids.models import Aid, AidProject, SuggestedAidProject
from aids.mixins import AidEditMixin, AidCopyMixin
from aids.utils import prepopulate_ds_folder
from projects.constants import EXPORT_FORMAT_KEYS
from aids.services.export import export_aids
from alerts.forms import AlertForm
from categories.models import Category
from minisites.mixins import SearchMixin, NarrowedFiltersMixin
from organizations.constants import ORGANIZATION_TYPES_SINGULAR_ALL
from programs.models import Program
from projects.models import Project
from projects.forms import ProjectExportForm
from geofr.models import Perimeter
from geofr.utils import get_all_related_perimeters
from blog.models import PromotionPost
from search.utils import clean_search_form
from stats.models import AidViewEvent
from stats.utils import log_aidviewevent, log_aidsearchevent
from core.utils import remove_accents

from accounts.tasks import (
    send_new_suggested_aid_notification_email,
    send_suggested_aid_denied_notification_email,
    send_suggested_aid_accepted_notification_email,
    send_new_aid_in_favorite_project_notification_email,
)
from analytics.utils import track_goal


class AidPaginator(Paginator):
    """Custom paginator for aids.

    The default django paginator uses COUNT(*) for counting results, which
    takes up a lot of memory and results in terrible performances.
    """

    @cached_property
    def count(self):
        return self.object_list.values("id").order_by("id").count()


class SearchView(SearchMixin, FormMixin, ListView):
    """Search and display aids."""

    template_name = "aids/search.html"
    context_object_name = "aids"
    form_class = AidSearchForm
    paginate_by = 18
    paginator_class = AidPaginator

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.form.full_clean()
        self.store_current_search()

        # Used to display a warning when a user first consults the page
        search_view_visits = request.session.get("search_view_visits", 0)
        request.session["search_view_visits"] = search_view_visits + 1
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Return the list of results to display."""

        financers_qs = Backer.objects.order_by("aidfinancer__order", "name")

        instructors_qs = Backer.objects.order_by("aidinstructor__order", "name")

        qs = (
            Aid.objects.published()
            .open()
            .select_related("perimeter", "author")
            .prefetch_related(Prefetch("financers", queryset=financers_qs))
            .prefetch_related(Prefetch("instructors", queryset=instructors_qs))
        )

        filter_form = self.form
        results = filter_form.filter_queryset(qs)
        ordered_results = filter_form.order_queryset(results).distinct()

        host = self.request.get_host()
        request_ua = self.request.META.get("HTTP_USER_AGENT", "")

        if (
            self.request.user
            and self.request.user.is_authenticated
            and self.request.user.beneficiary_organization
            and self.request.user.beneficiary_organization.organization_type[0]
            in [
                "commune",
                "epci",
                "department",
                "region",
                "special",
                "public_cies",
                "public_org",
            ]
        ):
            user = self.request.user
            org = user.beneficiary_organization
            log_aidsearchevent.delay(
                user_pk=user.pk,
                org_pk=org.pk,
                querystring=self.request.GET.urlencode(),
                results_count=ordered_results.count(),
                source=host,
                request_ua=request_ua,
            )
        else:
            log_aidsearchevent.delay(
                querystring=self.request.GET.urlencode(),
                results_count=ordered_results.count(),
                source=host,
                request_ua=request_ua,
            )

        return ordered_results

    def get_programs(self):
        """Get the aid programs that matched the search perimeter.

        We consider that there is a match in one of the two cases:

         - the searched perimeter exactly matches some program's perimeter;
         - the searched perimeter is contained in some program's perimeter.
        """

        searched_perimeter = self.form.cleaned_data.get("perimeter", None)
        if not searched_perimeter:
            return []

        q_exact_match = Q(perimeter=searched_perimeter)
        q_container_match = Q(perimeter__in=searched_perimeter.contained_in.all())
        programs = Program.objects.filter(q_exact_match | q_container_match)
        return programs

    def get_promotions(self):

        promotions = PromotionPost.objects.filter(status="published")

        searched_backers = self.form.cleaned_data.get("backers", None)
        if searched_backers:
            promotions = promotions.filter(
                Q(backers__in=searched_backers) | Q(backers__isnull=True)
            )
        else:
            promotions = promotions.filter(backers__isnull=True)

        searched_programs = self.form.cleaned_data.get("programs", None)
        if searched_programs:
            promotions = promotions.filter(
                Q(programs__in=searched_programs) | Q(programs__isnull=True)
            )
        else:
            promotions = promotions.filter(programs__isnull=True)

        searched_categories = self.form.cleaned_data.get("categories", None)
        if searched_categories:
            promotions = promotions.filter(
                Q(categories__in=searched_categories) | Q(categories__isnull=True)
            )
        else:
            promotions = promotions.filter(categories__isnull=True)

        searched_perimeter = self.form.cleaned_data.get("perimeter", None)
        if searched_perimeter:
            searched_perimeter = get_all_related_perimeters(
                searched_perimeter.id, values=["id"]
            )
            promotions = promotions.filter(
                Q(perimeter__in=searched_perimeter) | Q(perimeter__isnull=True)
            )
        else:
            promotions = promotions.filter(perimeter__isnull=True)

        searched_targeted_audiences = self.form.cleaned_data.get(
            "targeted_audiences", None
        )
        if searched_targeted_audiences:
            promotions = promotions.filter(
                Q(targeted_audiences__overlap=searched_targeted_audiences)
                | Q(targeted_audiences__isnull=True)
            )
        else:
            promotions = promotions.filter(targeted_audiences__isnull=True)

        promotions = promotions.distinct()

        return promotions

    def store_current_search(self):
        """Store the current search query in a cookie.

        This is needed to provide the correct "go back to your search" link in
        other pages' breadcrumbs.
        """
        current_search_query = self.request.GET.urlencode()
        if "targeted_audiences=&" in current_search_query:
            current_search_query = current_search_query.replace(
                "targeted_audiences=&", ""
            )
        self.request.session[settings.SEARCH_COOKIE_NAME] = current_search_query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        search_view_visits = self.request.session["search_view_visits"]

        if search_view_visits <= 1 and not user.is_authenticated:
            context["next_page_login_warning"] = True
        else:
            context["next_page_login_warning"] = False

        context["current_search"] = self.request.session.get(
            settings.SEARCH_COOKIE_NAME, ""
        )
        context["current_search_dict"] = clean_search_form(
            self.form.cleaned_data, remove_extra_fields=True
        )
        context["page_title"] = self.page_title()

        default_order = "relevance"
        order_value = self.request.GET.get("order_by", default_order)
        order_labels = dict(AidSearchForm.ORDER_BY_CHOICES)
        order_label = order_labels.get(order_value, order_labels[default_order])
        context["order_label"] = order_label
        context["alert_form"] = AlertForm(label_suffix="")
        context["promotions"] = self.get_promotions()

        return context

    def page_title(self):
        """
        Formats the <title> of the search page with the parameters
        """
        current_search_dict = clean_search_form(
            self.form.cleaned_data, remove_extra_fields=True
        )

        if not len(current_search_dict):
            return "Toutes les aides"

        output_array = []
        if "targeted_audiences" in current_search_dict:
            targeted_audience_raw = current_search_dict.pop("targeted_audiences")[0]

            targeted_audience = dict(ORGANIZATION_TYPES_SINGULAR_ALL)[
                targeted_audience_raw
            ]
            output_array.append(f"Structure : {targeted_audience}")

        if "perimeter" in current_search_dict:
            perimeter = current_search_dict.pop("perimeter")
            output_array.append(f"Périmètre : {perimeter.name}")

        if "text" in current_search_dict:
            text = current_search_dict.pop("text")
            if len(text) >= 50:
                text = text[:49] + "…"
            output_array.append(f"Mots-clés : {text}")

        other_criteria = len(current_search_dict)
        if other_criteria == 1:
            output_array.append(f"{len(current_search_dict)} autre critère")
        elif other_criteria > 1:
            output_array.append(f"{len(current_search_dict)} autres critères")

        return " - ".join(output_array)


class AdvancedSearchView(SearchMixin, NarrowedFiltersMixin, FormView):
    """Only displays the search form, more suitable for mobile views."""

    form_class = AdvancedAidFilterForm
    template_name = "aids/advanced_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_search"] = self.request.session.get(
            settings.SEARCH_COOKIE_NAME, ""
        )
        return context


class ResultsView(SearchView):
    """Only display search results.

    This view is designed to be called via AJAX, and only renders html
    fragment of search engine results.
    """

    template_name = "aids/_results.html"

    def get_context_data(self, **kwargs):
        kwargs["search_actions"] = True
        return super().get_context_data(**kwargs)


class ResultsReceiveView(LoginRequiredMixin, SearchView):
    """Send the search results by email."""

    http_method_names = ["post"]
    EMAIL_SUBJECT = "Vos résultats de recherche"

    def get_form_data(self):
        querydict = self.request.POST.copy()
        for key in ("csrfmiddlewaretoken", "integration"):
            try:
                querydict.pop(key)
            except KeyError:
                pass
        return querydict

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.get_form_data()
        return kwargs

    def post(self, request, *args, **kwargs):
        """Send those search results by email to the user.

        We do it synchronously, but this view is meant to be called from an
        AJAX query, so it should not be a problem.
        """
        self.form = self.get_form()
        self.form.full_clean()
        results = self.get_queryset()
        nb_results = results.count()
        first_results = results[:10]
        site = get_current_site(self.request)
        querystring = self.get_form_data().urlencode()
        scheme = "https"
        search_url = reverse("search_view")
        full_url = "{scheme}://{domain}{search_url}?{querystring}".format(
            scheme=scheme,
            domain=site.domain,
            search_url=search_url,
            querystring=querystring,
        )
        results_body = render_to_string(
            "emails/search_results.txt",
            {
                "user_name": self.request.user.full_name,
                "aids": first_results,
                "nb_results": nb_results,
                "full_url": full_url,
                "scheme": scheme,
                "domain": site.domain,
            },
        )
        send_mail(
            self.EMAIL_SUBJECT,
            results_body,
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=False,
        )
        return HttpResponse("")


class AidDetailView(DetailView):
    """Display an aid detail."""

    template_name = "aids/detail.html"
    context_object_name = "aid"

    def get_queryset(self):
        """Get the queryset.

        Since we want to enable aid preview, we have special cases depending
        on the current user:

         - anonymous or normal users can only see published aids.
         - contributors can see their own aids.
         - superusers can see all aids.
        """
        category_qs = Category.objects.select_related("theme").order_by(
            "theme__name", "name"
        )

        financers_qs = Backer.objects.order_by("aidfinancer__order", "name")

        instructors_qs = Backer.objects.order_by("aidinstructor__order", "name")

        base_qs = (
            Aid.objects.select_related("perimeter", "author")
            .prefetch_related(Prefetch("financers", queryset=financers_qs))
            .prefetch_related(Prefetch("instructors", queryset=instructors_qs))
            .prefetch_related("programs")
            .prefetch_related(Prefetch("categories", queryset=category_qs))
        )

        current_search = self.request.session.get(settings.SEARCH_COOKIE_NAME, "")
        if "targeted_audiences=&" in current_search:
            current_search = current_search.removeprefix("targeted_audiences=&")
        current_search_form = AidSearchForm(data=QueryDict(current_search))

        if current_search_form.is_valid():
            cleaned_search_data = clean_search_form(
                current_search_form.cleaned_data, remove_extra_fields=True
            )
            if "text" in cleaned_search_data:
                text = cleaned_search_data["text"]
                text = remove_accents(text)
                base_qs = (
                    base_qs.annotate(
                        headline_name=SearchHeadline(
                            "name",
                            SearchQuery(text, config="french_unaccent"),
                            config="french_unaccent",
                            start_sel="<mark>",
                            stop_sel="</mark>",
                            highlight_all=True,
                        )
                    )
                    .annotate(
                        headline_name_initial=SearchHeadline(
                            "name_initial",
                            SearchQuery(text, config="french_unaccent"),
                            config="french_unaccent",
                            start_sel="<mark>",
                            stop_sel="</mark>",
                            highlight_all=True,
                        )
                    )
                    .annotate(
                        headline_description=SearchHeadline(
                            "description",
                            SearchQuery(text, config="french_unaccent"),
                            config="french_unaccent",
                            start_sel="<mark>",
                            stop_sel="</mark>",
                            highlight_all=True,
                        )
                    )
                    .annotate(
                        headline_project_examples=SearchHeadline(
                            "project_examples",
                            SearchQuery(text, config="french_unaccent"),
                            config="french_unaccent",
                            start_sel="<mark>",
                            stop_sel="</mark>",
                            highlight_all=True,
                        )
                    )
                    .annotate(
                        headline_eligibility=SearchHeadline(
                            "eligibility",
                            SearchQuery(text, config="french_unaccent"),
                            config="french_unaccent",
                            start_sel="<mark>",
                            stop_sel="</mark>",
                            highlight_all=True,
                        )
                    )
                )

        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            qs = base_qs
        elif user.is_authenticated:
            q_published = Q(status="published")
            q_is_author = Q(author=user)
            qs = base_qs.filter(q_published | q_is_author)
        else:
            qs = base_qs.published()

        return qs

    def post_prepopulate_data(self, user, org):

        data = prepopulate_ds_folder(self.object.ds_mapping, user, org)
        ds_id = self.object.ds_id
        headers = {
            "Content-Type": "application/json",
        }
        post_url = f"https://www.demarches-simplifiees.fr/api/public/v1/demarches/{ds_id}/dossiers"
        response = requests.request("POST", post_url, json=data, headers=headers)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        current_search = self.request.session.get(settings.SEARCH_COOKIE_NAME, "")
        if "targeted_audiences=&" in current_search:
            current_search = current_search.removeprefix("targeted_audiences=&")

        context["current_search"] = current_search
        # Here we reconstruct the AidSearchForm from the current_search
        # querystring. This is needed to display some of the search filters.
        current_search_form = AidSearchForm(data=QueryDict(current_search))
        if current_search_form.is_valid():
            context["current_search_dict"] = clean_search_form(
                current_search_form.cleaned_data, remove_extra_fields=True
            )
            if "text" in clean_search_form(
                current_search_form.cleaned_data, remove_extra_fields=True
            ):
                context["text_search"] = clean_search_form(
                    current_search_form.cleaned_data, remove_extra_fields=True
                )["text"]

        if self.request.GET.get("open-modal"):
            context["open_modal"] = True

        context["programs"] = (
            self.object.programs.exclude(logo__isnull=True).exclude(logo="").distinct()
        )
        financers = self.object.financers.all()

        # We don't want to display instructors if they are the same as the
        # financers
        all_instructors = self.object.instructors.all()
        instructors = [i for i in all_instructors if i not in financers]
        context.update(
            {
                "financers": financers,
                "instructors": instructors,
            }
        )

        context["financers_with_logo"] = (
            financers.exclude(logo__isnull=True).exclude(logo="").distinct()
        )
        instructors_with_logo = [
            i for i in instructors if i.logo is not None and i.logo != ""
        ]
        context.update(
            {
                "instructors_with_logo": instructors_with_logo,
            }
        )

        """
        Aid imported from Ademe-Agir API contains sometimes an adhoc perimeter
        with unreadable name starting with "regions_" and regions-code list.
        In that case, we need to translate this name.
        """
        if (
            self.object.perimeter
            and self.object.perimeter.scale == 18
            and self.object.import_data_source
            and self.object.import_data_source.pk == 10
            and "regions_" in self.object.perimeter.name
        ):
            perimeter_name = self.object.perimeter.name.replace("regions_", "")
            perimeter_list = perimeter_name.split("_")
            regions_list = []
            for region_code in perimeter_list:
                try:
                    perimeter = Perimeter.objects.get(
                        code=region_code, scale=Perimeter.SCALES.region
                    )
                    regions_list.append(perimeter.name)
                except Exception:
                    try:
                        perimeter = Perimeter.objects.get(code=region_code)
                        regions_list.append(perimeter.name)
                    except Exception:
                        print(f"Code région : {region_code}")
            regions_names = ", ".join(sorted(regions_list))
            context["readable_adhoc_perimeter"] = regions_names

        context["eligibility_criteria"] = any(
            (
                self.object.mobilization_steps,
                self.object.destinations,
                self.object.project_examples,
                self.object.eligibility,
            )
        )

        categories = self.object.categories.all()
        keywords = self.object.keywords.all()
        categories_keywords_list = []
        for cat in categories:
            categories_keywords_list.append(cat.name)
        for keyword in keywords:
            categories_keywords_list.append(keyword.name)
        context["keywords"] = sorted(categories_keywords_list)

        context["alert_form"] = AlertForm(label_suffix="")

        if self.object.ds_schema_exists:
            if user.is_authenticated:
                if user.beneficiary_organization:
                    org = user.beneficiary_organization
                    org_type = org.organization_type

                    if org_type == ["commune"] or org_type == ["epci"]:
                        response = self.post_prepopulate_data(user, org)
                        if response:
                            context["prepopulate_application_url"] = json.loads(
                                response.content
                            )["dossier_url"]
                            context["ds_folder_id"] = json.loads(response.content)[
                                "dossier_id"
                            ]
                            context["ds_folder_number"] = json.loads(response.content)[
                                "dossier_number"
                            ]
            else:
                context["prepopulate_application_url"] = False
                context["ds_application_url"] = True
        else:
            context["prepopulate_application_url"] = False
            context["ds_application_url"] = False

        if user.is_authenticated:
            context["aid_match_project_form"] = AidMatchProjectForm(label_suffix="")
            context["suggest_aid_form"] = SuggestAidMatchProjectForm
            context["aid_detail_page"] = True
            if user.beneficiary_organization:
                context["projects"] = Project.objects.filter(
                    organizations=user.beneficiary_organization.pk
                ).order_by("name")
                context["favorite_projects"] = Project.objects.filter(
                    organization_favorite=user.beneficiary_organization,
                    is_public=True,
                    status=Project.STATUS.published,
                ).order_by("name")
                context["aid_projects"] = self.object.projects.all()

            search_preferences = user.get_search_preferences()
            context["user_targeted_audiences"] = search_preferences[
                "targeted_audiences"
            ]
            context["user_perimeter"] = search_preferences["perimeter"]

        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.object.is_published():
            current_search = response.context_data.get("current_search", "")
            host = request.get_host()
            request_ua = request.META.get("HTTP_USER_AGENT", "")
            request_referer = request.META.get("HTTP_REFERER", "")
            if (
                self.request.user
                and self.request.user.is_authenticated
                and self.request.user.beneficiary_organization
                and self.request.user.beneficiary_organization.organization_type[0]
                in [
                    "commune",
                    "epci",
                    "department",
                    "region",
                    "special",
                    "public_cies",
                    "public_org",
                    "researcher",
                ]
            ):
                user = self.request.user
                org = user.beneficiary_organization
                log_aidviewevent.delay(
                    aid_id=self.object.id,
                    user_pk=user.pk,
                    org_pk=org.pk,
                    querystring=current_search,
                    source=host,
                    request_ua=request_ua,
                    request_referer=request_referer,
                )
            else:
                log_aidviewevent.delay(
                    aid_id=self.object.id,
                    querystring=current_search,
                    source=host,
                    request_ua=request_ua,
                    request_referer=request_referer,
                )

        return response


class AidDraftListView(
    ContributorAndProfileCompleteRequiredMixin, AidEditMixin, ListView
):
    """Display the list of aids published by the user."""

    template_name = "aids/draft_list.html"
    context_object_name = "aids"
    paginate_by = 50
    sortable_columns = [
        "name",
        "perimeter__name",
        "date_created",
        "date_updated",
        "submission_deadline",
        "status",
    ]
    default_ordering = "-date_updated"

    def get_queryset(self):
        qs = super().get_queryset()

        filter_form = DraftListAidFilterForm(self.request.GET)

        if filter_form.is_valid():
            state = filter_form.cleaned_data["state"]
            if state:
                if state == "open":
                    qs = qs.open()
                elif state == "deadline":
                    qs = qs.soon_expiring()
                elif state == "expired":
                    qs = qs.expired()

            display_status = filter_form.cleaned_data["display_status"]
            if display_status:
                if display_status == "hidden":
                    qs = qs.hidden()
                if display_status == "live":
                    qs = qs.live()

        return qs

    def get_ordering(self):
        order = self.request.GET.get("order", "")
        order_field = order.lstrip("-")
        if order_field not in self.sortable_columns:
            order = self.default_ordering
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = DraftListAidFilterForm(self.request.GET)
        context["ordering"] = self.get_ordering()
        aid_ids = context["aids"].values_list("id", flat=True)

        events = AidViewEvent.objects.filter(aid_id__in=aid_ids)

        events_total_count = events.count()

        recent_30_days_ago = timezone.now() - timedelta(days=30)
        events_last_30_days_count = events.filter(
            date_created__gte=recent_30_days_ago
        ).count()

        events_total_count_per_aid = (
            events.values_list("aid_id")
            .annotate(view_count=Count("aid_id"))
            .order_by("aid_id")
        )

        context["hits_total"] = events_total_count
        context["hits_last_30_days"] = events_last_30_days_count
        context["hits_per_aid"] = dict(events_total_count_per_aid)
        context["form"] = ProjectExportForm

        return context


class AidCreateView(ContributorAndProfileCompleteRequiredMixin, CreateView):
    """Allows publishers to submit their own aids."""

    template_name = "aids/create.html"
    form_class = AidEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        # The value of this flag is given to the form and will change
        # the way the form data is validated.
        # When the aid is saved as a draft, we don't enforce a full validity,
        # to allow users to save incomplete data.
        kwargs["requested_status"] = self.request.POST.get("_status", None)
        return kwargs

    def form_valid(self, form):
        self.object = aid = form.save(commit=False)

        requested_status = self.request.POST.get("_status", None)
        if requested_status == "reviewable":
            aid.status = "reviewable"

        aid.author = self.request.user
        aid.save()
        form.save_m2m()

        msg = f"""Votre aide a été créée. Vous pouvez poursuivre l’édition ou
        <a href="{aid.get_absolute_url()}" target="_blank">la prévisualiser
        <span class="fr-sr-only">Ouvre une nouvelle fenêtre</span></a>."""

        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        edit_url = reverse("aid_edit_view", args=[self.object.slug])
        return edit_url


class AidEditView(
    ContributorAndProfileCompleteRequiredMixin,
    MessageMixin,
    AidEditMixin,
    UpdateView,
    AidCopyMixin,
):
    """Edit an existing aid."""

    template_name = "aids/edit.html"
    context_object_name = "aid"
    form_class = AidEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        # There are several submit buttons that have different actions
        # The user can save the form, save as a duplicate, or save and
        # publish / unpublish the aid.
        # Depending on the action, the aid object will be
        # given a different status
        action = self.request.POST.get("_action", None)

        # Duplicates must be saved as drafts
        if action == "save_as_new":
            kwargs["requested_status"] = "draft"

        # Drafts can pass in review
        # Aids in review or published can go back to draft
        elif action == "update_status":
            if self.object.status == "draft":
                kwargs["requested_status"] = "review"
            else:
                kwargs["requested_status"] = "draft"

        # Normal form saving, keep current status untouched
        else:
            kwargs["requested_status"] = None

        return kwargs

    def form_valid(self, form):

        action = self.request.POST.get("_action", None)

        if action == "save_as_new":
            obj = form.save(commit=False)
            obj = self.copy_aid(obj)
            form.save_m2m()
            msg = f"""La nouvelle aide a été créée. Vous pouvez poursuivre l’édition.
            Et retrouvez l’aide dupliquée sur
            <a href="{reverse('aid_draft_list_view')}">votre portefeuille d’aides</a>."""
            response = HttpResponseRedirect(self.get_success_url())
        else:

            response = super().form_valid(form)

            if action == "update_status":
                aid = self.object
                if aid.is_draft():
                    aid.submit()
                    msg = "Votre aide est actuellement en revue. Elle sera publiée et visible par les utilisateurs du site une fois que l’administrateur l’aura validée."  # noqa
                else:
                    aid.unpublish()
                    msg = "Le changement de statut de votre aide a bien été pris en compte."
            else:
                msg = "L’aide a bien été mise à jour. Vous pouvez poursuivre l’édition."

        self.messages.success(msg)
        return response

    def get_success_url(self):
        edit_url = reverse("aid_edit_view", args=[self.object.slug])
        return "{}".format(edit_url)


class AidDeleteView(
    ContributorAndProfileCompleteRequiredMixin, AidEditMixin, DeleteView
):
    """Soft deletes an existing aid."""

    def get_success_url(self):
        return reverse("aid_draft_list_view")

    def form_valid(self, form):
        """
        Overriding by not calling the super() method
        to prevent actual deletion of the aid
        """
        self.object = self.get_object()
        confirmed = self.request.POST.get("confirm", False)
        if confirmed:
            self.object.soft_delete()
            msg = "Votre aide a été supprimée."
            messages.success(self.request, msg)

        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class GenericToLocalAidView(
    ContributorAndProfileCompleteRequiredMixin,
    MessageMixin,
    AidCopyMixin,
    SingleObjectMixin,
    RedirectView,
):
    """Copy a generic aid into a local aid."""

    http_method_names = ["post"]

    def get_queryset(self):
        qs = Aid.objects.filter(is_generic=True)
        self.queryset = qs
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        existing_aid = self.get_object()
        new_aid = self.copy_aid(existing_aid)

        # At this point, the new aid is created and we want to
        # add specific data for local aid.
        existing_aid = self.get_object()
        new_aid.author = self.request.user
        new_aid.name = existing_aid.name
        new_aid.is_generic = False
        new_aid.generic_aid = existing_aid
        new_aid.clone_m2m(source_aid=existing_aid)
        new_aid.save()

        self.new_aid = new_aid
        msg = "Cette aide a été dupliquée"
        self.messages.success(msg)
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("aid_edit_view", args=[self.new_aid.slug])


class AidMatchProjectView(ContributorAndProfileCompleteRequiredMixin, UpdateView):
    """Associate aid to existing projects."""

    template_name = "projects/_match_aid_modal.html"
    form_class = AidMatchProjectForm
    context_object_name = "aid"
    model = Aid

    def form_valid(self, form):

        aid = form.save(commit=False)
        url = reverse("aid_detail_view", args=[aid.slug])

        if self.request.POST.getlist("projects"):
            # associate the existing projects to the aid
            for project in self.request.POST.getlist("projects", []):
                project = int(project)
                aid.projects.add(
                    project, through_defaults={"creator": self.request.user}
                )

                aid.save()

                # retrieve project's data to create successful message
                project_obj = Project.objects.get(pk=project)
                project_name = project_obj.name
                project_slug = project_obj.slug
                project_url = reverse(
                    "project_detail_view", args=[project, project_slug]
                )

                user = self.request.user

                # send email to aid_suggester
                if self.request.POST.get("_page", None) == "suggested_aid":
                    suggestedaidproject_obj = SuggestedAidProject.objects.get(
                        aid=aid.pk, project=project_obj.pk
                    )
                    suggestedaidproject_obj.is_associated = True
                    suggestedaidproject_obj.date_associated = timezone.now()
                    suggestedaidproject_obj.save()
                    url = project_url
                    send_suggested_aid_accepted_notification_email.delay(
                        project_author_organization_name=user.beneficiary_organization.name,
                        suggester_user_email=suggestedaidproject_obj.creator.email,
                        project_id=project_obj.pk,
                        suggested_aid_id=aid.pk,
                    )

                # send email to project_followers if exist
                organizations_favorite = project_obj.organization_favorite.all()
                if organizations_favorite:
                    for organization_favorite in organizations_favorite:
                        for (
                            project_follower
                        ) in organization_favorite.beneficiaries.all():
                            send_new_aid_in_favorite_project_notification_email(
                                project_author_email=user.email,
                                project_follower_email=project_follower.email,
                                project_id=project_obj.pk,
                                aid_name=aid.name,
                            )

                # send notification to other org members
                user = self.request.user
                other_members = project_obj.organization.beneficiaries.exclude(
                    id=user.id
                )
                for member in other_members:
                    member.send_notification(
                        title="Nouvelle aide ajoutée à un projet",
                        message=f"""
                        <p>
                            {user.full_name} a ajouté une aide au projet
                            <a href="{project_obj.get_absolute_url()}">{project_obj.name}</a>.
                        </p>
                        """,
                    )

                msg = f"L’aide a bien été associée au projet <a href='{project_url}'>{project_name}.</a>"  # noqa
                messages.success(self.request, msg)

        if self.request.POST.get("new_project"):
            user = self.request.user
            user_organization = user.beneficiary_organization
            # create the new project's object
            project = Project.objects.create(name=self.request.POST.get("new_project"))
            project.author.add(user)
            project.organizations.add(user_organization)

            # associate this new project's object to the aid
            aid.projects.add(
                project.pk, through_defaults={"creator": self.request.user}
            )
            aid.date_updated = aid.date_updated
            aid.save()
            project_url = reverse(
                "project_detail_view", args=[project.pk, project.slug]
            )

            # send notification to other org members
            other_members = user_organization.beneficiaries.exclude(id=user.id)
            for member in other_members:
                member.send_notification(
                    title="Un projet a été créé",
                    message=f"""
                    <p>
                        {user.full_name} a créé le projet
                        <a href="{project.get_absolute_url()}">{project.name}</a>.
                    </p>
                    """,
                )

            msg = f"Votre nouveau projet <a href='{project_url}'>{project.name}</a> a bien été créé et l’aide a été associée."  # noqa
            messages.success(self.request, msg)

        return HttpResponseRedirect(url)


class AidUnmatchProjectView(ContributorAndProfileCompleteRequiredMixin, UpdateView):
    """remove the association between an aid and a project."""

    context_object_name = "aid"
    form_class = AidMatchProjectForm
    model = Aid

    def form_valid(self, form):

        aid = form.save(commit=False)
        project_pk = int(self.request.POST.get("project-pk"))
        aid.projects.remove(project_pk)
        aid.date_updated = aid.date_updated
        aid.save()

        # send notification to other org members
        project_obj = Project.objects.get(pk=project_pk)
        user = self.request.user
        other_members = project_obj.organization.beneficiaries.exclude(id=user.id)
        for member in other_members:
            member.send_notification(
                title="Une aide a été supprimée d’un projet",
                message=f"""
                <p>
                    {user.full_name} a supprimé une aide du projet
                    <a href="{project_obj.get_absolute_url()}">{project_obj.name}</a>.
                </p>
                """,
            )

        msg = "L’aide a bien été supprimée."
        messages.success(self.request, msg)
        project_slug = self.request.POST.get("project-slug")
        url = reverse("project_detail_view", args=[project_pk, project_slug])
        return HttpResponseRedirect(url)


class SuggestAidMatchProjectView(ContributorAndProfileCompleteRequiredMixin, FormView):
    """Associate a suggested aid to an existing project."""

    form_class = SuggestAidMatchProjectForm

    def get_origin_page(self):
        if self.request.session.get("origin_page", None):
            origin_page = self.request.session.get("origin_page", None)
        else:
            self.request.session["origin_page"] = self.request.POST.get(
                "origin_page", None
            )
            origin_page = self.request.session.get("origin_page", None)
        return origin_page

    def form_valid(self, form):
        aid = form.cleaned_data["aid"]
        projects = form.cleaned_data["project"]
        user = self.request.user

        if projects and aid:
            try:
                for project in projects:
                    if project.is_public and project.status == Project.STATUS.published:
                        aid.suggested_projects.add(
                            project.pk, through_defaults={"creator": self.request.user}
                        )
                        aid.save()
                        send_new_suggested_aid_notification_email.delay(
                            project_author_email=project.author.first().email,
                            suggester_user_email=user.email,
                            suggester_organization_name=user.beneficiary_organization.name,
                            project_id=project.id,
                            suggested_aid_id=aid.id,
                        )
                        track_goal(self.request.session, settings.GOAL_REGISTER_ID)
                    else:
                        raise PermissionDenied()
            except Exception:
                raise PermissionDenied()

        origin_page = self.get_origin_page()

        if origin_page == "aid_detail_page":
            success_url = reverse("aid_detail_view", args=[aid.slug])
        elif origin_page == "favorite_project_page":
            success_url = reverse(
                "favorite_project_detail_view", args=[project.pk, project.slug]
            )
        else:
            success_url = reverse(
                "public_project_detail_view", args=[project.pk, project.slug]
            )

        del self.request.session["origin_page"]
        msg = "Merci! L’aide a bien été suggérée!"
        messages.success(self.request, msg)

        return HttpResponseRedirect(success_url)

    def get_template_names(self):
        origin_page = self.get_origin_page()

        if origin_page == "aid_detail_page":
            return ["aids/detail.html"]
        elif origin_page == "favorite_project_page":
            return ["projects/favorite_project_detail.html"]
        else:
            return ["projects/public_project_detail.html"]

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        error = "erreur"

        post_values = self.request.POST.copy()
        post_values["origin_page"] = self.get_origin_page()
        post_values["aid"] = form.data["aid"]
        post_values["project"] = form.data["project"]
        form = SuggestAidMatchProjectForm(post_values)

        origin_page = self.get_origin_page()

        if origin_page == "aid_detail_page":
            aid = Aid.objects.get(slug=form.data["aid"])
            project = None
        else:
            aid = None
            project = Project.objects.get(pk=form.data["project"])

        return self.render_to_response(
            self.get_context_data(
                suggest_aid_form=form,
                error_aid=error,
                project=project,
                aid=aid,
            ),
        )


class SuggestedAidUnmatchProjectView(
    ContributorAndProfileCompleteRequiredMixin, UpdateView
):
    """remove the association between a suggested aid and a project."""

    context_object_name = "aid"
    form_class = AidMatchProjectForm
    model = Aid

    def form_valid(self, form):

        aid = form.save(commit=False)
        project_pk = int(self.request.POST.get("project-pk"))
        suggested_aidproject = SuggestedAidProject.objects.get(
            aid=aid.pk, project=project_pk
        )
        suggested_aidproject.is_rejected = True
        suggested_aidproject.date_rejected = timezone.now()
        suggested_aidproject.save()
        user = self.request.user
        send_suggested_aid_denied_notification_email.delay(
            project_author_organization_name=user.beneficiary_organization.name,
            suggester_user_email=suggested_aidproject.creator.email,
            project_id=project_pk,
            suggested_aid_id=aid.pk,
        )
        track_goal(self.request.session, settings.GOAL_REGISTER_ID)

        msg = "L’aide a bien été supprimée de la liste des aides suggérées pour votre projet."
        messages.success(self.request, msg)
        project_slug = self.request.POST.get("project-slug")
        url = reverse("project_detail_view", args=[project_pk, project_slug])
        return HttpResponseRedirect(url)


class AidProjectStatusView(ContributorAndProfileCompleteRequiredMixin, UpdateView):
    """Allow user to precise if they requested and obtained the aid for the project or not"""

    context_object_name = "aidproject"
    form_class = AidProjectStatusForm
    model = AidProject

    def get_template_names(self):

        return ["projects/project_detail.html"]

    def form_valid(self, form):

        aidproject = form.save(commit=False)

        user_organization = self.request.user.beneficiary_organization
        if aidproject.creator.beneficiary_organization != user_organization:
            raise PermissionDenied()

        if form.cleaned_data["aid_requested"] is True:
            form.date_requested = timezone.now()
        else:
            form.date_requested = None

        if form.cleaned_data["aid_obtained"] is True:
            form.date_obtained = timezone.now()
        else:
            form.date_obtained = None

        if form.cleaned_data["aid_paid"] is True:
            form.date_paid = timezone.now()
        else:
            form.date_paid = None

        if form.cleaned_data["aid_denied"] is True:
            form.date_denied = timezone.now()
        else:
            form.date_denied = None

        form.save()

        msg = f"Le statut de l’aide «{aidproject.aid.name}» a bien été mis à jour."
        messages.success(self.request, msg)
        url = reverse(
            "project_detail_view", args=[aidproject.project.pk, aidproject.project.slug]
        )
        return HttpResponseRedirect(url)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(
            self.get_context_data(
                user=self.request.user,
                aid_set=self.object.project.aid_set.all(),
                AidProject=AidProject.objects.filter(project=self.object.project),
                SuggestedAidProject=SuggestedAidProject.objects.filter(
                    project=self.object.project.pk
                ),
                suggested_aid=self.object.project.suggested_aid.filter(
                    suggestedaidproject__is_associated=False,
                    suggestedaidproject__is_rejected=False,
                ),
                aid_project_status_form=AidProjectStatusForm(self.request.POST),
                error_aidproject_status=self.object.pk,
                project=self.object.project,
                aidproject=self.object,
                form=ProjectExportForm,
            ),
        )


class AidExportView(ContributorAndProfileCompleteRequiredMixin, View):
    """Export all organization's aids."""

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        file_format = self.request.POST["format"]
        org = self.request.user.beneficiary_organization.pk

        if file_format in EXPORT_FORMAT_KEYS:
            response_data = export_aids(org, file_format)
            if "error" not in response_data:
                filename = response_data["filename"]
                return HttpResponse(
                    response_data["content"],
                    content_type=response_data["content_type"],
                    headers={
                        "Content-Disposition": f'attachment; filename="{filename}"'
                    },
                )
        # If something went wrong, redirect to the aid draft list page with an error
        messages.error(
            self.request,
            f"""
            Impossible de générer votre export. Si le problème persiste, merci de
            <a href="{reverse('contact')}"/>nous contacter</a>.
            """,
        )
        return HttpResponseRedirect(reverse("aid_draft_list_view"))
