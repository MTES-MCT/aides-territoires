import json
from django.views.generic import TemplateView
from django.utils.text import slugify
from django.core.serializers import serialize

from map.utils import get_backers_count_by_department, get_programs_count_by_department
from geofr.models import Perimeter
from organizations.constants import ORGANIZATION_TYPE


class MapView(TemplateView):
    template_name = "map/map.html"

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

        return context


class DepartmentView(TemplateView):
    template_name = "map/department.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = departments.get(code=kwargs["code"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        backers_list = get_backers_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)
        programs_list = get_programs_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        captions = {
            "backers": f"Top 10 des {backers_list.count()} porteurs :",
            "programs": f"Top 10 des {programs_list.count()} programmes :"
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
    template_name = "map/department_backers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = departments.get(code=kwargs["code"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        backers_list = get_backers_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        context["departments"] = departments
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["aid_type"] = aid_type
        context["backers_list"] = backers_list
 
        return context

class DepartmentProgramsView(TemplateView):
    template_name = "map/department_programs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = departments.get(code=kwargs["code"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        programs_list = get_programs_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        context["departments"] = departments
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["aid_type"] = aid_type
        context["programs_list"] = programs_list
 
        return context
