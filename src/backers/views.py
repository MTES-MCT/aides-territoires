from django.views.generic import ListView
from django.http import Http404

from backers.models import Backer
from aids.models import Aid
from programs.models import Program
from categories.models import Category
from aids.views import AidPaginator
from stats.utils import log_backerviewevent


class BackerDetailView(ListView):
    template_name = "backers/detail.html"
    context_object_name = "aids"
    paginate_by = 18
    paginator_class = AidPaginator

    def get(self, request, *args, **kwargs):

        if "pk" in self.kwargs:
            backer = self.kwargs.get("pk")

            qs = Backer.objects.filter(pk=backer)
            try:
                obj = qs.get()
            except qs.model.DoesNotExist:
                raise Http404()

            self.backer = obj

        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        qs = (
            Aid.objects.live()
            .filter(financers=self.backer.id)
            .prefetch_related("financers")
        )

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
            log_backerviewevent.delay(
                backer_id=self.backer.pk,
                user_pk=user.pk,
                org_pk=org.pk,
                source=host,
                request_ua=request_ua,
                request_referer=request_referer,
            )
        else:
            log_backerviewevent.delay(
                backer_id=self.backer.pk,
                source=host,
                request_ua=request_ua,
                request_referer=request_referer,
            )

        return qs

    def get_context_data(self, **kwargs):

        backer = self.backer
        aids = self.object_list
        categories = (
            Category.objects.filter(aids__in=aids)
            .select_related("theme")
            .order_by("theme")
            .distinct()
        )
        categories = [
            {"name": category.name, "theme": category.theme} for category in categories
        ]
        programs = Program.objects.filter(aids__in=aids).distinct()

        context = super().get_context_data(**kwargs)
        context["backer"] = backer
        context["programs"] = programs
        context["categories"] = categories
        context["backer_page"] = True

        return context
