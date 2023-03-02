from django.views.generic import DetailView

from backers.models import Backer
from aids.models import Aid
from programs.models import Program
from categories.models import Category


class BackerDetailView(DetailView):
    context_object_name = "backer"
    template_name = "backers/detail.html"
    queryset = Backer.objects.all()

    def get_context_data(self, **kwargs):

        aids = (
            Aid.objects.live()
            .filter(financers=self.object.id)
            .prefetch_related("financers")
        )
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
        context["aids"] = aids
        context["programs"] = programs
        context["categories"] = categories
        context["backer_page"] = True

        return context
