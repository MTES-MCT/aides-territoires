import json

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin

from minisites.mixins import SearchMixin

from geofr.forms.forms import BackerByDepartmentForm
from geofr.models import Perimeter
from backers.models import Backer
from programs.models import Program


class MapView(TemplateView):
    template_name = "geofr/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments_list = Perimeter.objects.departments(
            values=["id", "name", "code", "backers_count"]
        )

        context["departments"] = departments_list
        context["departments_json"] = json.dumps(departments_list)
        context["backers_count"] = Backer.objects.has_financed_aids().count()
        context["programs_count"] = Program.objects.has_aids().count()

        return context


class DepartmentBackersView(SearchMixin, FormMixin, ListView):
    template_name = "geofr/department_backers.html"
    form_class = BackerByDepartmentForm
    context_object_name = "backers"

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.form.full_clean()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Return the list of results to display."""

        filter_form = self.form
        results = filter_form.filter_queryset(
            self.request.resolver_match.kwargs["code"]
        ).distinct()

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments_list = Perimeter.objects.departments(values=["id", "name", "code"])
        current_dept = [
            dep
            for dep in departments_list
            if dep["code"] == self.request.resolver_match.kwargs["code"]
        ][0]

        aid_type = self.request.GET.get("aid_type")

        if aid_type == "financial_group":
            caption_aid_type = " financières"
        elif aid_type == "technical_group":
            caption_aid_type = " en ingénierie"
        else:
            caption_aid_type = ""
        caption = f"{current_dept['name'] } : {self.object_list.count()} "
        caption += f"porteurs d‘aides{caption_aid_type} présents"

        context["departments"] = departments_list
        context["current_dept"] = current_dept
        context["caption"] = caption

        return context
