from django.views.generic import ListView, DetailView

from programs.models import Program


class ProgramList(ListView):
    template_name = 'programs/list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        qs = Program.objects.all()
        return qs


class ProgramDetail(DetailView):
    template_name = 'programs/detail.html'
    context_object_name = 'program'

    def get_queryset(self):
        qs = Program.objects.all()
        return qs
