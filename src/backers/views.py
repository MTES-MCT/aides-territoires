import json
from django.db.models import Exists, OuterRef
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import ListView

from accounts.mixins import ContributorAndProfileCompleteRequiredMixin
from accounts.models import User
from aids.models import Aid
from aids.views import AidPaginator
from backers.models import Backer
from categories.models import Category
from geofr.utils import get_all_related_perimeters
from programs.models import Program
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
            .select_related("perimeter")
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


class BackersBlacklistView(ContributorAndProfileCompleteRequiredMixin, ListView):
    template_name = "backers/blacklist.html"
    paginate_by = 20

    def get_queryset(self):

        user = self.request.user
        user_org = user.beneficiary_organization
        perimeter = user_org.perimeter
        target_audience = user_org.organization_type[0]

        related_perimeters = get_all_related_perimeters(perimeter.id, values=["id"])
        live_aids = Aid.objects.live()

        qs = (
            Backer.objects.prefetch_related("financed_aids")
            .select_related("perimeter")
            .filter(
                perimeter_id__in=related_perimeters,
                financed_aids__in=live_aids,
                financed_aids__perimeter_id__in=related_perimeters,
                financed_aids__targeted_audiences__overlap=[target_audience],
            )
            .annotate(
                is_masked=Exists(
                    User.masked_backers.through.objects.filter(
                        backer_id=OuterRef("pk"), user_id=user.pk
                    )
                )
            )
            .distinct()
            .order_by(("name"))
        )

        qs = qs.annotate_aids_count(
            Backer.financed_aids, "nb_financed_aids"
        ).annotate_aids_count(Backer.instructed_aids, "nb_instructed_aids")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["backers"] = self.object_list
        return context


class ToggleBackerMaskView(ContributorAndProfileCompleteRequiredMixin, View):
    def post(self, request, pk):
        """
        Method called from the front-end through an Ajax post
        """
        user = request.user
        backer = get_object_or_404(Backer, pk=pk)
        is_masked = json.loads(request.POST.get("masked", "false"))
        user.toggle_masked_backer(backer=backer, is_masked=is_masked)
        print(is_masked, type(is_masked))

        return JsonResponse({"status": "success"})
