from django.db.models.signals import pre_delete
from django.dispatch import receiver

from accounts.models import User


@receiver(pre_delete, sender=User, dispatch_uid="user_delete_signal")
def manage_user_content_before_deletion(sender, instance, **kwargs):
    """
    Some user-generated content must be managed on user account deletion.

    Part of this management is delegated to the DeleteUserView, which allows the user
    to make some extra deletions.

    - ALERTS:   User can chose to delete some alerts along with their account.
                Otherwise, they are kept → nothing to do here

    - AIDS:     Aids are protected and thus must be managed outside of the pre_delete
                (else the delete() method will never go there)

    Using a pre_delete signal https://docs.djangoproject.com/en/3.2/ref/signals/#django.db.models.signals.pre_delete
    """

    user = instance
    user_org = user.beneficiary_organization

    # PROJECTS: Reattributed to another user belonging to the user's organization if such a user exists.
    # Otherwise, the projects are deleted.
    new_author = user_org.beneficiaries.exclude(id=user.id).first()

    projects = user_org.project_set.filter(author=user)
    if new_author:
        for project in projects:
            project.author.add(new_author)
            project.author.remove(user)
            project.save()
    else:
        projects.delete()

    # INVITATIONS (to the organization) : The form allows the user to reattribute them to another
    #  user. Otherwise, they are deleted.
    invited_users = User.objects.filter(invitation_author_id=user)

    for invited_user in invited_users:
        invited_user.proposed_organization_id = None
        invited_user.invitation_author_id = None
        invited_user.invitation_date = None
        invited_user.save()

    # ORGANIZATION: if the user is alone in their organization, it must be deleted too.
    if not new_author:
        user.beneficiary_organization = None
        user.save()
        user_org.delete()
