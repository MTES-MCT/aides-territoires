from django.views.generic import DetailView

from django.db.models import Prefetch

from backers.models import Backer
from aids.models import Aid
from programs.models import Program
from categories.models import Category


class BackerDetailView(DetailView):
    context_object_name = "backer"
    template_name = "backers/detail.html"
    queryset = Backer.objects.all()

    def get_context_data(self, **kwargs):

        categories_list = Category.objects.select_related("theme")
        aids = (
            Aid.objects.live()
            .filter(financers=self.object.id)
            .prefetch_related(Prefetch("categories", queryset=categories_list))
            .order_by("categories__theme", "categories__name")
        )
        categories = Category.objects.filter(aids__in=aids).order_by("theme").distinct()

        categories = [
            {"name": category.name, "theme": category.theme} for category in categories
        ]

        programs = (
            Program.objects.filter(aids__in=aids)
            .exclude(logo__isnull=True)
            .exclude(logo="")
            .distinct()
        )

        context = super().get_context_data(**kwargs)
        context["aids"] = aids
        context["programs"] = programs
        context["categories"] = categories

        return context
