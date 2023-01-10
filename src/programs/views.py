from django.views.generic import ListView, DetailView

from programs.models import Program
from aids.models import Aid
from pages.models import Tab


class ProgramList(ListView):
    template_name = "programs/list.html"
    context_object_name = "programs"

    def get_queryset(self):
        qs = Program.objects.all()
        return qs


class ProgramDetail(DetailView):
    template_name = "programs/detail.html"
    context_object_name = "program"
    queryset = Program.objects.all()

    def get_context_data(self, **kwargs):

        aids = Aid.objects.live().filter(programs=self.object.id)

        context = super().get_context_data(**kwargs)
        context["aids"] = aids
        context["program_tabs"] = Tab.objects.filter(program=self.object)
        if self.request.GET.get("tab") == "faq":
            context["faq_selected"] = True

        return context
