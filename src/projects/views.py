from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect
from braces.views import MessageMixin

from projects.forms import ProjectSuggestForm


class ProjectSuggest(MessageMixin, CreateView):
    """Allows users to suggest their own projects."""

    template_name = 'projects/_suggest_modal.html'
    form_class = ProjectSuggestForm
    context_object_name = 'project'

    def form_valid(self, form):

        project = form.save(commit=False)
        project.date_created = timezone.now()
        project.is_suggested = True

        project.save()
        form.save_m2m()

        msg = _('Your suggestion will be reviewed by an admin soon. '
                'Thank you for contributing.')
        self.messages.success(msg)
        url = reverse('search_step_project')
        return HttpResponseRedirect(url)
