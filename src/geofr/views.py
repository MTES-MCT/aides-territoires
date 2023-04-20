import json

from django.views.generic import TemplateView

from backers.models import Backer
from geofr.services.counts_by_department import (
    get_backers_count_by_department,
    get_programs_count_by_department,
)
from geofr.models import Perimeter
from organizations.constants import ORGANIZATION_TYPE_CHOICES
from programs.models import Program


class MapView(TemplateView):
    template_name = "geofr/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments_list = Perimeter.objects.departments(
            values=["id", "name", "code", "backers_count", "programs_count"]
        )

        context["departments"] = departments_list
        context["departments_json"] = json.dumps(departments_list)
        context["backers_count"] = Backer.objects.has_financed_aids().count()
        context["programs_count"] = Program.objects.has_aids().count()

        return context


class DepartmentView(TemplateView):
    template_name = "geofr/department.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments_list = Perimeter.objects.departments(values=["id", "name", "code"])
        current_dept = [
            dep for dep in departments_list if dep["code"] == kwargs["code"]
        ][0]

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")
        perimeter_scale = self.request.GET.get("perimeter_scale")

        backers_list = get_backers_count_by_department(
            current_dept["id"],
            target_audience=target_audience,
            aid_type=aid_type,
            perimeter_scale=perimeter_scale,
        )
        programs_list = get_programs_count_by_department(
            current_dept["id"], target_audience=target_audience, aid_type=aid_type
        )

        captions = {
            "backers": f"Top 10 des {backers_list.count()} porteurs par nombre d’aides :",
            "programs": f"Top 10 des {programs_list.count()} programmes par nombre d’aides :",
        }

        context["departments"] = departments_list
        context["organization_types"] = ORGANIZATION_TYPE_CHOICES
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["backers_list"] = backers_list
        context["programs_list"] = programs_list
        context["captions"] = captions
        context["aid_type"] = aid_type
        context["perimeter_scale"] = perimeter_scale

        return context


class DepartmentBackersView(TemplateView):
    template_name = "geofr/department_backers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments_list = Perimeter.objects.departments(values=["id", "name", "code"])
        current_dept = [
            dep for dep in departments_list if dep["code"] == kwargs["code"]
        ][0]

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")
        perimeter_scale = self.request.GET.get("perimeter_scale")

        backers_list = get_backers_count_by_department(
            current_dept["id"],
            target_audience=target_audience,
            aid_type=aid_type,
            perimeter_scale=perimeter_scale,
        )

        if aid_type == "financial_group":
            caption_aid_type = " financières"
        elif aid_type == "technical_group":
            caption_aid_type = " en ingénierie"
        else:
            caption_aid_type = ""
        caption = f"{current_dept['name'] } : {backers_list.count()} "
        caption += f"porteurs d‘aides{caption_aid_type} présents"

        context["departments"] = departments_list
        context["organization_types"] = ORGANIZATION_TYPE_CHOICES
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["aid_type"] = aid_type
        context["perimeter_scale"] = perimeter_scale
        context["backers_list"] = backers_list
        context["caption"] = caption

        return context


class DepartmentProgramsView(TemplateView):
    template_name = "geofr/department_programs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments_list = Perimeter.objects.departments(values=["id", "name", "code"])
        current_dept = [
            dep for dep in departments_list if dep["code"] == kwargs["code"]
        ][0]

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        programs_list = get_programs_count_by_department(
            current_dept["id"], target_audience=target_audience, aid_type=aid_type
        )

        if aid_type == "financial_group":
            caption_aid_type = " financiers"
        elif aid_type == "technical_group":
            caption_aid_type = " techniques"
        else:
            caption_aid_type = ""
        caption = f"{current_dept['name'] } : {programs_list.count()} "
        caption += f"programmes{caption_aid_type} présents"

        context["departments"] = departments_list
        context["organization_types"] = ORGANIZATION_TYPE_CHOICES
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["aid_type"] = aid_type
        context["programs_list"] = programs_list
        context["caption"] = caption

        return context
