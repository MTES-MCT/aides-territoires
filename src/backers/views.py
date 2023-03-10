from django.views.generic import ListView
from django.http import Http404

from backers.models import Backer
from aids.models import Aid
from programs.models import Program
from categories.models import Category
from aids.views import AidPaginator


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
