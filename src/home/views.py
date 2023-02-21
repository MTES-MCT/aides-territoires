import json

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from aids.forms import AidSearchForm
from aids.models import Aid
from backers.models import Backer
from blog.models import BlogPost
from categories.models import Category
from geofr.models import Perimeter
from home.forms import ContactForm
from home.tasks import send_contact_form_email
from organizations.models import Organization
from programs.models import Program
from projects.models import Project
from projects.forms import ProjectSearchForm
from stats.utils import log_contactformsendevent


class HomeView(FormView):
    """Display the home page, as well as some other pages
    (contact form, mailing list registration form, ...)

    Said mailing list is directly posted to the email provider, so we don't
    have to process it ourselves.

    """

    http_method_names = ["get"]
    template_name = "home/home.html"
    context_object_name = "aids"
    form_class = AidSearchForm

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.form.full_clean()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        financers_qs = Backer.objects.order_by("aidfinancer__order", "name")
        instructors_qs = Backer.objects.order_by("aidinstructor__order", "name")
        programs_qs = Program.objects.order_by("-date_created")
        organizations_qs = Organization.objects.all().select_related("perimeter")
        categories_qs = Category.objects.all().select_related("theme")
        aids_qs = (
            Aid.objects.live()
            .select_related("perimeter")
            .prefetch_related(Prefetch("financers", queryset=financers_qs))
            .prefetch_related(Prefetch("instructors", queryset=instructors_qs))
            .prefetch_related(Prefetch("programs", queryset=programs_qs))
        )
        selected_backers = financers_qs.can_be_displayed_on_homepage()
        # We only display 5 at random
        subset_selected_backers = selected_backers.order_by("?")[0:5]

        selected_programs = programs_qs.can_be_displayed_on_homepage()
        # We only display the latest 3
        subset_selected_programs = selected_programs[0:3]

        context = super().get_context_data(**kwargs)
        context["nb_aids"] = aids_qs.values("id").count()
        context["nb_categories"] = categories_qs.count()
        context["nb_backers"] = financers_qs.has_financed_aids().count()
        context["nb_programs"] = programs_qs.has_aids().count()
        context["subset_selected_backers"] = subset_selected_backers
        context["subset_selected_programs"] = subset_selected_programs
        context["skiplinks"] = [{"link": "#intro", "label": "Contenu"}]
        context["public_projects"] = (
            Project.objects.filter(is_public=True, status=Project.STATUS.published)
            .prefetch_related(Prefetch("organizations", queryset=organizations_qs))
            .prefetch_related("project_types")
            .order_by("-date_created")[:3]
        )
        context["project_form"] = ProjectSearchForm
        context["recent_aids"] = aids_qs.order_by("-date_created")[:3]
        context["recent_posts"] = BlogPost.objects.published()[:2]

        # Map section
        departments_list = Perimeter.objects.departments(
            values=["id", "name", "code", "backers_count", "programs_count"]
        )
        context["departments"] = departments_list
        context["departments_json"] = json.dumps(departments_list)

        context["project_form"] = ProjectSearchForm

        return context

    def get_initial(self):
        # if user is authenticated
        # and if user organization type and user organization's perimeter are defined
        # we pre-populate targeted_audience & perimeter fields

        if self.request.user.is_authenticated:
            initial = self.request.user.get_search_preferences()
            return initial


class ContactView(SuccessMessageMixin, FormView):
    """Display the contact form."""

    form_class = ContactForm
    template_name = "home/contact.html"
    success_message = "Votre message a bien été envoyé, merci !"
    success_url = reverse_lazy("contact")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["first_name"] = self.request.user.first_name
            initial["last_name"] = self.request.user.last_name
            initial["email"] = self.request.user.email
        return initial

    def form_valid(self, form):
        """Send the content of the form via email."""
        response = super().form_valid(form)
        form_dict = form.cleaned_data

        # Only send the message if the honeypot field is empty
        if form_dict["website"] == "":
            send_contact_form_email.delay(form_dict)
            log_contactformsendevent.delay(
                subject=form_dict["subject"],
            )
        # track_goal(self.request.session, settings.GOAL_CONTACT_ID)
        return response


class NewsletterConfirmView(TemplateView):
    """Display success message after register action."""

    template_name = "home/newsletter_confirm.html"


class NewsletterSuccessView(TemplateView):
    """Display success message after register action."""

    template_name = "home/newsletter_success.html"


class ADDNAOptin(TemplateView):
    """Display a welcome message to users from addna."""

    template_name = "home/addna_optin.html"
