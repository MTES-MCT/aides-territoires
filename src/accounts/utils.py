from django.db.models.query import QuerySet
from django.contrib.auth.hashers import check_password
from django.forms import ValidationError

from accounts.models import User


def check_current_password(entered_password, registered_password):
    """Check if the user entered a valid password"""
    if not entered_password:
        raise ValidationError(
            "Vous devez entrer votre mot de passe actuel pour pouvoir le changer."
        )
    else:
        if check_password(entered_password, registered_password):
            return True
        else:
            raise ValidationError("Le mot de passe actuel entré est incorrect.")


def cancel_invitation(invited_user: User) -> None:
    """Cancels a pending invitaiton to a user"""
    invited_user.proposed_organization_id = None
    invited_user.invitation_author_id = None
    invited_user.invitation_date = None
    invited_user.save()


def cancel_invitations(invited_users: QuerySet) -> None:
    """Cancels pending invitations to a group of users"""
    for invited_user in invited_users:
        cancel_invitation(invited_user)
