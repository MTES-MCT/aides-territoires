from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.core.exceptions import PermissionDenied
from braces.views import MessageMixin

from aids.models import Aid
from aids.services.export import export_related_projects


class ExportRelatedProjects(MessageMixin, SingleObjectMixin, View):
    """Export related projects for a specific aid with a csv file."""

    def get_queryset(self):
        qs = Aid.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        object_id = int(self.kwargs["object_id"])
        aid = Aid.objects.get(pk=object_id)
        user = self.request.user
        if not user.is_superuser:
            raise PermissionDenied()

        response_data = export_related_projects(aid)

        if "error" in response_data:
            # If something went wrong, redirect to the aid detail stats page with an error
            self.messages.error(
                self.request,
                """
                Impossible de générer votre export. Si le problème persiste, merci de
                contacter l'équipe technique.
                """,
            )
            pass
        else:
            return response_data
