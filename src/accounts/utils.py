from django.forms import ValidationError

from django.contrib.auth.hashers import check_password


def check_current_password(entered_password, registered_password):
    """Check if the user entered a valid password"""
    if not entered_password:
        raise ValidationError(
            "Vous devez entrer votre mot de passe actuel pour pouvoir le changer.")
    else:
        if check_password(entered_password, registered_password):
            return True
        else:
            raise ValidationError("Le mot de passe actuel entré est incorrect.")
