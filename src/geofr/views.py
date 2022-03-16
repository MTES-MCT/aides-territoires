import json
from django.views.generic import TemplateView
from django.utils.text import slugify
from backers.models import Backer

from geofr.services.counts_by_department import get_backers_count_by_department, get_programs_count_by_department
from geofr.models import Perimeter
from organizations.constants import ORGANIZATION_TYPE
from programs.models import Program


class MapView(TemplateView):
    template_name = "geofr/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department).values(
            "id", "name", "code", "backers_count", "programs_count")

        # perimeters currently don't have a proper slug
        departments_list = []
        for department in departments:
            department['slug'] = slugify(department['name'])
            departments_list.append(department)

        context["departments"] = departments
        context["departments_list"] = json.dumps(departments_list)
        context['backers_count'] = Backer.objects.has_financed_aids().count()
        context['programs_count'] = Program.objects.count()

        return context


class DepartmentView(TemplateView):
    template_name = "geofr/department.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = departments.get(code=kwargs["code"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        backers_list = get_backers_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)
        programs_list = get_programs_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        captions = {
            "backers": f"Top 10 des {backers_list.count()} porteurs par nombre d’aides :",
            "programs": f"Top 10 des {programs_list.count()} programmes par nombre d’aides :"
        }

        context["departments"] = departments
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["backers_list"] = backers_list
        context["programs_list"] = programs_list
        context["captions"] = captions
        context["aid_type"] = aid_type

        return context


class DepartmentBackersView(TemplateView):
    template_name = "geofr/department_backers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = departments.get(code=kwargs["code"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        backers_list = get_backers_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        if aid_type == "financial":
            caption_aid_type = " financières"
        elif aid_type == "technical":
            caption_aid_type = " en ingénierie"
        else:
            caption_aid_type =  ""
        caption = f"{current_dept.name } : {backers_list.count()} porteurs d‘aides{caption_aid_type} présents"

        context["departments"] = departments
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["aid_type"] = aid_type
        context["backers_list"] = backers_list
        context["caption"] = caption
 
        return context

class DepartmentProgramsView(TemplateView):
    template_name = "geofr/department_programs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = departments.get(code=kwargs["code"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        programs_list = get_programs_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        if aid_type == "financial":
            caption_aid_type = " financiers"
        elif aid_type == "technical":
            caption_aid_type = " techniques"
        else:
            caption_aid_type =  ""
        caption = f"{current_dept.name } : {programs_list.count()} programmes{caption_aid_type} présents"

        context["departments"] = departments
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["aid_type"] = aid_type
        context["programs_list"] = programs_list
        context["caption"] = caption
 
        return context
