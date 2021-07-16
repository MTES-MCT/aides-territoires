from django.utils import timezone

from aids.models import Aid, AidWorkflow
from aids.utils import generate_clone_title


def aid_author_queryset(user):
    return Aid.objects \
        .filter(author=user) \
        .select_related('perimeter') \
        .order_by('name')


def aid_author_or_colleague_queryset(user):
    return Aid.objects \
        .filter(author__backer=user.backer) \
        .select_related('perimeter') \
        .order_by('name')


class AidAuthorMixin:
    """Common code to aid editing views."""

    def get_queryset(self):
        self.queryset = aid_author_queryset(self.request.user)
        return super().get_queryset()


class AidAuthorOrColleagueMixin:
    """Common code to aid editing views."""

    def get_queryset(self):
        if not self.request.user.backer:
            self.queryset = aid_author_queryset(self.request.user)
        else:
            self.queryset = aid_author_or_colleague_queryset(self.request.user)
        return super().get_queryset()


class AidCopyMixin:
    """Common code for helping with copy/duplicate operations."""

    def copy_aid(self, existing_aid):
        new_aid = existing_aid
        new_aid.id = None
        new_aid.name = generate_clone_title(existing_aid.name)
        new_aid.slug = None
        new_aid.date_created = timezone.now()
        new_aid.date_published = None
        new_aid.status = AidWorkflow.states.draft
        new_aid.is_imported = False
        new_aid.import_uniqueid = None
        new_aid.save()
        return new_aid
