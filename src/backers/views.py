from django.views.generic import DetailView, TemplateView

from django.db.models import Prefetch

from backers.models import Backer
from aids.models import Aid
from backers.utils import get_backers_count_by_departement
from programs.models import Program
from categories.models import Category
from geofr.models import Perimeter
from organizations.constants import ORGANIZATION_TYPE


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


class BackerMapView(TemplateView):
    template_name = "backers/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departements = Perimeter.objects.filter(scale=10)

        context["departements"] = departements

        return context


class BackerDepartementView(TemplateView):
    template_name = "backers/departement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departements = Perimeter.objects.filter(scale=10)
        current_dept = Perimeter.objects.get(code=kwargs["code"], scale=10)

        backers_list = get_backers_count_by_departement(current_dept.id)

        context["departements"] = departements
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["backers_list"] = backers_list

        return context


class BackerDepartementBackersView(TemplateView):
    template_name = "backers/departement_backers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departements = Perimeter.objects.filter(scale=10)
        current_dept = Perimeter.objects.get(code=kwargs["code"], scale=10)

        backers_list = get_backers_count_by_departement(current_dept.id)

        context["departements"] = departements
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["backers_list"] = backers_list

        return context
