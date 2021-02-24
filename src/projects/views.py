from django.views.generic import CreateView
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.http import urlencode
from django.urls import reverse
from django.http import HttpResponseRedirect
from braces.views import MessageMixin

from projects.forms import ProjectSuggestForm
from categories.models import Category


class ProjectSuggest(MessageMixin, CreateView):
    """Allows users to suggest their own projects."""

    template_name = 'projects/_suggest_modal.html'
    form_class = ProjectSuggestForm
    context_object_name = 'project'

    def form_valid(self, form):

        querystring = self.request.GET.urlencode()
        categories_list = self.request.GET.getlist('categories', '')
        categories = Category.objects.filter(slug__in=categories_list).values_list('id', flat=True)

        project = form.save(commit=False)
        project.date_created = timezone.now()
        project.is_suggested = True

        project.save()
        form.save_m2m()
        project.categories.add(*categories)

        msg = _('Your suggestion will be reviewed by an admin soon. '
                'Thank you for contributing.')
        self.messages.success(msg)
        url = reverse('search_step_project')
        url = '{}?{}'.format(url, querystring)
        return HttpResponseRedirect(url)
