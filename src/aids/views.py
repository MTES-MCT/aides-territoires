from datetime import timedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q, Count, Prefetch
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, ListView, UpdateView,
                                  RedirectView, DeleteView, FormView)
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils.functional import cached_property
from django.core.mail import send_mail

from braces.views import MessageMixin

from accounts.mixins import ContributorRequiredMixin
from backers.models import Backer
from aids.forms import (AidEditForm, AidSearchForm,
                        AdvancedAidFilterForm, DraftListAidFilterForm)
from aids.models import Aid, AidWorkflow
from aids.tasks import log_admins
from aids.utils import generate_clone_title
from aids.mixins import AidEditMixin
from alerts.forms import AlertForm
from categories.models import Category
from minisites.mixins import SearchMixin, NarrowedFiltersMixin
from programs.models import Program
from search.utils import clean_search_form
from stats.models import AidViewEvent
from stats.utils import (log_aidviewevent, log_aidsearchevent)


class AidPaginator(Paginator):
    """Custom paginator for aids.

    The default django paginator uses COUNT(*) for counting results, which
    takes up a lot of memory and results in terrible performances.
    """

    @cached_property
    def count(self):
        return self.object_list.values('id').order_by('id').count()


class SearchView(SearchMixin, FormMixin, ListView):
    """Search and display aids."""

    template_name = 'aids/search.html'
    context_object_name = 'aids'
    form_class = AidSearchForm
    paginate_by = 18
    paginator_class = AidPaginator

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.form.full_clean()
        self.store_current_search()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Return the list of results to display."""

        financers_qs = Backer.objects \
            .order_by('aidfinancer__order', 'name')

        instructors_qs = Backer.objects \
            .order_by('aidinstructor__order', 'name')

        qs = Aid.objects \
            .published() \
            .open() \
            .select_related('perimeter', 'author') \
            .prefetch_related(Prefetch('financers', queryset=financers_qs)) \
            .prefetch_related(Prefetch('instructors',
                                       queryset=instructors_qs)) \

        filter_form = self.form
        results = filter_form.filter_queryset(qs)
        ordered_results = filter_form.order_queryset(results).distinct()

        host = self.request.get_host()
        log_aidsearchevent.delay(
            querystring=self.request.GET.urlencode(),
            results_count=ordered_results.count(),
            source=host)

        return ordered_results

    def get_programs(self):
        """Get the aid programs that matched the search perimeter.

        We consider that there is a match in one of the two cases:

         - the searched perimeter exactly matches some program's perimeter;
         - the searched perimeter is contained in some program's perimeter.
        """

        searched_perimeter = self.form.cleaned_data.get('perimeter', None)
        if not searched_perimeter:
            return []

        q_exact_match = Q(perimeter=searched_perimeter)
        q_container_match = Q(
            perimeter__in=searched_perimeter.contained_in.all())
        programs = Program.objects \
            .filter(q_exact_match | q_container_match)
        return programs

    def store_current_search(self):
        """Store the current search query in a cookie.

        This is needed to provide the correct "go back to your search" link in
        other pages' breadcrumbs.
        """
        current_search_query = self.request.GET.urlencode()
        self.request.session[settings.SEARCH_COOKIE_NAME] = current_search_query  # noqa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['current_search'] = self.request.session.get(
            settings.SEARCH_COOKIE_NAME, '')
        context['current_search_dict'] = clean_search_form(
            self.form.cleaned_data, remove_extra_fields=True)

        default_order = 'relevance'
        order_value = self.request.GET.get('order_by', default_order)
        order_labels = dict(AidSearchForm.ORDER_BY)
        order_label = order_labels.get(
            order_value, order_labels[default_order])
        context['order_label'] = order_label
        context['alert_form'] = AlertForm(label_suffix='')

        return context


class AdvancedSearchView(SearchMixin, NarrowedFiltersMixin, FormView):
    """Only displays the search form, more suitable for mobile views."""

    form_class = AdvancedAidFilterForm
    template_name = 'aids/advanced_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_search'] = self.request.session.get(
            settings.SEARCH_COOKIE_NAME, '')
        return context


class ResultsView(SearchView):
    """Only display search results.

    This view is designed to be called via ajax, and only renders html
    fragment of search engine results.
    """
    template_name = 'aids/_results.html'

    def get_context_data(self, **kwargs):
        kwargs['search_actions'] = True
        return super().get_context_data(**kwargs)


class ResultsReceiveView(LoginRequiredMixin, SearchView):
    """Send the search results by email."""

    http_method_names = ['post']
    EMAIL_SUBJECT = 'Vos résultats de recherche'

    def get_form_data(self):
        querydict = self.request.POST.copy()
        for key in ('csrfmiddlewaretoken', 'integration'):
            try:
                querydict.pop(key)
            except KeyError:
                pass
        return querydict

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.get_form_data()
        return kwargs

    def post(self, request, *args, **kwargs):
        """Send those search results by email to the user.

        We do it synchronously, but this view is meant to be called from an
        ajax query, so it should not be a problem.
        """
        self.form = self.get_form()
        self.form.full_clean()
        results = self.get_queryset()
        nb_results = results.count()
        first_results = results[:10]
        site = get_current_site(self.request)
        querystring = self.get_form_data().urlencode()
        scheme = 'https'
        search_url = reverse('search_view')
        full_url = '{scheme}://{domain}{search_url}?{querystring}'.format(
            scheme=scheme,
            domain=site.domain,
            search_url=search_url,
            querystring=querystring)
        results_body = render_to_string('emails/search_results.txt', {
            'user_name': self.request.user.full_name,
            'aids': first_results,
            'nb_results': nb_results,
            'full_url': full_url,
            'scheme': scheme,
            'domain': site.domain,
        })
        send_mail(
            self.EMAIL_SUBJECT,
            results_body,
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=False)
        return HttpResponse('')


class AidDetailView(DetailView):
    """Display an aid detail."""

    template_name = 'aids/detail.html'

    def get_queryset(self):
        """Get the queryset.

        Since we want to enable aid preview, we have special cases depending
        on the current user:

         - anonymous or normal users can only see published aids.
         - contributors can see their own aids.
         - superusers can see all aids.
        """
        category_qs = Category.objects \
            .select_related('theme') \
            .order_by('theme__name', 'name')

        financers_qs = Backer.objects \
            .order_by('aidfinancer__order', 'name')

        instructors_qs = Backer.objects \
            .order_by('aidinstructor__order', 'name')

        base_qs = Aid.objects \
            .select_related('perimeter', 'author') \
            .prefetch_related(Prefetch('financers', queryset=financers_qs)) \
            .prefetch_related(Prefetch('instructors',
                                       queryset=instructors_qs)) \
            .prefetch_related('programs') \
            .prefetch_related(Prefetch('categories', queryset=category_qs))

        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            qs = base_qs
        elif user.is_authenticated:
            q_published = Q(status='published')
            q_is_author = Q(author=user)
            qs = base_qs.filter(q_published | q_is_author)
        else:
            qs = base_qs.published()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_search = self.request.session.get(
             settings.SEARCH_COOKIE_NAME, '')
        context['current_search'] = current_search
        # Here we reconstruct the AidSearchForm from the current_search
        # querystring. This is needed to display some of the search filters.
        current_search_form = AidSearchForm(data=QueryDict(current_search))
        if current_search_form.is_valid():
            context['current_search_dict'] = clean_search_form(
                current_search_form.cleaned_data, remove_extra_fields=True)

        context['programs'] = self.object.programs \
            .exclude(logo__isnull=True) \
            .exclude(logo='') \
            .distinct()
        financers = self.object.financers.all()

        # We don't want to display instructors if they are the same as the
        # financers
        all_instructors = self.object.instructors.all()
        instructors = [i for i in all_instructors if i not in financers]
        context.update({
            'financers': financers,
            'instructors': instructors,
        })

        context['financers_with_logo'] = financers \
            .exclude(logo__isnull=True) \
            .exclude(logo='') \
            .distinct()

        context['eligibility_criteria'] = any((
            self.object.mobilization_steps,
            self.object.destinations,
            self.object.project_examples,
            self.object.eligibility))

        context['alert_form'] = AlertForm(label_suffix='')

        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.object.is_published():
            host = request.get_host()
            current_search = response.context_data.get('current_search', '')
            log_aidviewevent.delay(
                aid_id=self.object.id,
                querystring=current_search,
                source=host)

        return response


class AidDraftListView(ContributorRequiredMixin, AidEditMixin, ListView):
    """Display the list of aids published by the user."""

    template_name = 'aids/draft_list.html'
    context_object_name = 'aids'
    paginate_by = 50
    sortable_columns = [
        'name',
        'perimeter__name',
        'date_created',
        'date_updated',
        'submission_deadline',
        'status',
    ]
    default_ordering = '-date_updated'

    def get_queryset(self):
        qs = super().get_queryset()

        filter_form = DraftListAidFilterForm(self.request.GET)

        if filter_form.is_valid():
            state = filter_form.cleaned_data['state']
            if state:
                if state == 'open':
                    qs = qs.open()
                elif state == 'deadline':
                    qs = qs.soon_expiring()
                elif state == 'expired':
                    qs = qs.expired()

            display_status = filter_form.cleaned_data['display_status']
            if display_status:
                if display_status == 'hidden':
                    qs = qs.hidden()
                if display_status == 'live':
                    qs = qs.live()

        return qs

    def get_ordering(self):
        order = self.request.GET.get('order', '')
        order_field = order.lstrip('-')
        if order_field not in self.sortable_columns:
            order = self.default_ordering
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = DraftListAidFilterForm(self.request.GET)
        context['ordering'] = self.get_ordering()
        aid_ids = context['aids'].values_list('id', flat=True)

        events = AidViewEvent.objects.filter(aid_id__in=aid_ids)

        events_total_count = events.count()

        recent_30_days_ago = timezone.now() - timedelta(days=30)
        events_last_30_days_count = events \
            .filter(date_created__gte=recent_30_days_ago) \
            .count()

        events_total_count_per_aid = events \
            .values_list('aid_id') \
            .annotate(view_count=Count('aid_id')) \
            .order_by('aid_id')

        context['hits_total'] = events_total_count
        context['hits_last_30_days'] = events_last_30_days_count
        context['hits_per_aid'] = dict(events_total_count_per_aid)

        return context


class AidCreateView(ContributorRequiredMixin, CreateView):
    """Allows publishers to submit their own aids."""

    template_name = 'aids/create.html'
    form_class = AidEditForm

    def form_valid(self, form):
        self.object = aid = form.save(commit=False)

        requested_status = self.request.POST.get('status', None)
        if requested_status == 'review':
            aid.status = 'reviewable'

        aid.author = self.request.user
        aid.save()
        form.save_m2m()

        msg = _('Your aid was sucessfully created. You can keep editing it or '
                '<a href="%(url)s" target="_blank">preview it</a>.') % {
                    'url': aid.get_absolute_url()
                }

        messages.success(self.request, msg)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        edit_url = reverse('aid_edit_view', args=[self.object.slug])
        return edit_url


class AidEditView(ContributorRequiredMixin, MessageMixin, AidEditMixin,
                  UpdateView):
    """Edit an existing aid."""

    template_name = 'aids/edit.html'
    context_object_name = 'aid'
    form_class = AidEditForm

    def form_valid(self, form):

        save_as_new = '_save_as_new' in self.request.POST
        if save_as_new:
            obj = form.save(commit=False)
            obj.id = None
            obj.slug = None
            obj.date_created = timezone.now()
            obj.date_published = None
            obj.status = AidWorkflow.states.draft
            obj.is_imported = False
            obj.import_uniqueid = None
            obj.name = generate_clone_title(obj.name)
            obj.save()
            form.save_m2m()
            msg = _('The new aid was sucessfully created. '
                    'You can keep editing it. And find the duplicated '
                    'aid in <a href="%(url)s">your portfolio</a>.') % {
                        'url': reverse('aid_draft_list_view')
                    }

            response = HttpResponseRedirect(self.get_success_url())
        else:
            response = super().form_valid(form)
            msg = _('The aid was sucessfully updated. You can keep '
                    'editing it.')

        self.messages.success(msg)
        return response

    def get_success_url(self):
        edit_url = reverse('aid_edit_view', args=[self.object.slug])
        return '{}'.format(edit_url)


class AidStatusUpdate(ContributorRequiredMixin, AidEditMixin,
                      SingleObjectMixin, RedirectView):
    """Update an aid status."""

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.update_aid_status()
        return super().post(request, *args, **kwargs)

    def update_aid_status(self):
        """Move the aid to the next step in the workflow.

        None of these transitions require any special permission, hence we
        don't run any additional checks.
        """
        aid = self.object

        # Check that submitted form data is still consistent
        current_status = self.request.POST.get('current_status', None)
        if aid.status != current_status:
            return

        STATES = AidWorkflow.states
        if aid.status == STATES.draft:
            aid.submit()
            msg = _('Your aid will be reviewed by an admin soon. '
                    'It will be published and visible for users '
                    'once an admin has approved it.')
        elif aid.status in (STATES.reviewable, STATES.published):
            aid.unpublish()
            log_admins.delay(
                'Aide dépubliée',
                'Une aide vient d\'être dépubliée.\n\n{}'.format(aid),
                aid.get_absolute_url())
            msg = _('We updated your aid status.')

        messages.success(self.request, msg)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('aid_edit_view', args=[self.object.slug])


class AidDeleteView(ContributorRequiredMixin, AidEditMixin, DeleteView):
    """Soft deletes an existing aid."""

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirmed = self.request.POST.get('confirm', False)
        if confirmed:
            self.object.soft_delete()
            msg = _('Your aid was deleted.')
            messages.success(self.request, msg)

        success_url = reverse('aid_draft_list_view')
        redirect = HttpResponseRedirect(success_url)
        return redirect
