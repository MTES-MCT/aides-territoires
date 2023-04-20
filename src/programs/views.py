from django.views.generic import ListView
from django.db.models import Prefetch
from django.http import Http404

from programs.models import Program
from aids.models import Aid
from pages.models import FaqQuestionAnswer, Tab
from aids.views import SearchView
from backers.models import Backer
from aids.views import AidPaginator
from stats.utils import log_programviewevent


class ProgramList(ListView):
    template_name = "programs/list.html"
    context_object_name = "programs"

    def get_queryset(self):
        qs = Program.objects.all()
        return qs


class ProgramDetail(SearchView):
    template_name = "programs/detail.html"
    context_object_name = "aids"
    paginate_by = 18
    paginator_class = AidPaginator

    def get(self, request, *args, **kwargs):

        if "slug" in self.kwargs:
            program = self.kwargs.get("slug")

            qs = Program.objects.filter(slug=program)
            try:
                obj = qs.get()
            except qs.model.DoesNotExist:
                raise Http404()

            self.program = obj

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Filter the queryset on the categories and audiences filters."""

        financers_qs = Backer.objects.order_by("aidfinancer__order", "name")

        instructors_qs = Backer.objects.order_by("aidinstructor__order", "name")

        # Start from the base queryset and add-up more filtering

        qs = (
            Aid.objects.published()
            .open()
            .filter(programs=self.program.pk)
            .select_related("perimeter", "author")
            .prefetch_related(Prefetch("financers", queryset=financers_qs))
            .prefetch_related(Prefetch("instructors", queryset=instructors_qs))
        )

        filter_form = self.form
        results = filter_form.filter_queryset(qs)

        host = self.request.get_host()
        request_ua = self.request.META.get("HTTP_USER_AGENT", "")
        request_referer = self.request.META.get("HTTP_REFERER", "")

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
            log_programviewevent.delay(
                program_id=self.program.pk,
                user_pk=user.pk,
                org_pk=org.pk,
                source=host,
                request_ua=request_ua,
                request_referer=request_referer,
            )
        else:
            log_programviewevent.delay(
                program_id=self.program.pk,
                source=host,
                request_ua=request_ua,
                request_referer=request_referer,
            )

        return results

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["program"] = self.program
        context["program_tabs"] = Tab.objects.filter(program=self.program)
        if self.program.pk == 36:
            context["program_fonds_vert"] = True
        context["tab_selected"] = self.request.GET.get("tab")
        if self.request.GET.get("tab") == "faq":
            context["faq_selected"] = True
        faq_questions_answers = FaqQuestionAnswer.objects.filter(
            program=self.program.pk
        ).select_related("faq_category")
        context["faq_questions_answers"] = faq_questions_answers
        if faq_questions_answers:
            context[
                "faq_questions_answers_date_updated"
            ] = faq_questions_answers.latest("date_updated").date_updated

        return context
