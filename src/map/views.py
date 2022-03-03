from django.views.generic import TemplateView

from map.utils import get_backers_count_by_department, get_programs_count_by_department
from geofr.models import Perimeter
from organizations.constants import ORGANIZATION_TYPE


class MapView(TemplateView):
    template_name = "map/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)

        context["departments"] = departments

        return context


class DepartmentView(TemplateView):
    template_name = "map/department.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = Perimeter.objects.get(id=kwargs["pk"])

        target_audience = self.request.GET.get("target_audience")

        if target_audience:
            backers_list = get_backers_count_by_department(current_dept.id, target_audience)
            programs_list = get_programs_count_by_department(current_dept.id, target_audience)
        else:
            backers_list = get_backers_count_by_department(current_dept.id)
            programs_list = get_programs_count_by_department(current_dept.id)

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

        return context


class DepartmentBackersView(TemplateView):
    template_name = "map/department_backers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        departments = Perimeter.objects.filter(scale=Perimeter.SCALES.department)
        current_dept = Perimeter.objects.get(id=kwargs["pk"])

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
        current_dept = Perimeter.objects.get(id=kwargs["pk"])

        target_audience = self.request.GET.get("target_audience")
        aid_type = self.request.GET.get("aid_type")

        programs_list = get_programs_count_by_department(current_dept.id, target_audience=target_audience, aid_type=aid_type)

        context["departments"] = departments
        context["organization_types"] = ORGANIZATION_TYPE
        context["current_dept"] = current_dept
        context["target_audience"] = target_audience
        context["programs_list"] = programs_list
 
        return context
