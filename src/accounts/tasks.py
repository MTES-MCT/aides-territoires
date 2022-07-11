from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlencode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings

from core.utils import get_base_url
from core.celery import app
from accounts.models import User
from emails.utils import send_email, send_email_with_template


LOGIN_SUBJECT = "Connexion à Aides-territoires"


@app.task
def send_connection_email(
    user_email, body_template="emails/login_token.txt", reset_password=False
):
    """Send a login email to the user.

    The email contains a token that can be used once to login.

    We use the default django token generator, that is usually used for
    password resets.
    """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    user_uid = urlsafe_base64_encode(force_bytes(user.pk))
    login_token = default_token_generator.make_token(user)
    login_url = reverse("token_login", args=[user_uid, login_token])
    base_url = get_base_url()
    if reset_password is False:
        full_login_url = f"{base_url}{login_url}"
        login_subject = LOGIN_SUBJECT
    else:
        next_url = {"next": "password_reset_confirm"}
        full_login_url = f"{base_url}{login_url}?{urlencode(next_url)}"
        body_template = "emails/reset_password.txt"
        login_subject = "Renouvellement de votre mot de passe"

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "user_name": user.full_name,
            "full_login_url": full_login_url,
        },
    )
    send_email(
        subject=login_subject,
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )


@app.task
def send_welcome_email(user_email):
    """Send a welcome email to the user.

    This email is actually stored as a template in the SendinBlue's dashboard,
    and can be modified by the bizdev team.

    Hence we don't define any email body ourselves.
    """
    if not settings.SIB_WELCOME_EMAIL_ENABLED:
        return

    user = User.objects.get(email=user_email)
    data = {
        "PRENOM": user.first_name,
        "NOM": user.last_name,
    }

    if user.is_contributor and user.is_beneficiary:
        template_id = settings.SIB_WELCOME_MIXTE_EMAIL_TEMPLATE_ID,
    elif user.is_contributor:
        template_id = settings.SIB_WELCOME_CONTRIBUTOR_EMAIL_TEMPLATE_ID,
    elif user.is_beneficiary:
        template_id = settings.SIB_WELCOME_BENEFICIARY_EMAIL_TEMPLATE_ID,

    send_email_with_template(
        recipient_list=[user_email],
        template_id=template_id,
        data=data,
        tags=["bienvenue", settings.ENV_NAME],
        fail_silently=True,
    )


@app.task
def send_invitation_email(
    user_email,
    invitator_name,
    organization_name,
    body_template="emails/invite_login_token.txt",
):
    """Send a login email to the user invited.

    The email contains a token that can be used once to login.

    We use the default django token generator, that is usually used for
    password resets.
    """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    user_uid = urlsafe_base64_encode(force_bytes(user.pk))
    login_token = default_token_generator.make_token(user)
    login_url = reverse("token_login", args=[user_uid, login_token])
    base_url = get_base_url()
    full_login_url = "{base_url}{url}".format(base_url=base_url, url=login_url)

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "invitator_name": invitator_name,
            "organization_name": organization_name,
            "user_name": user.full_name,
            "full_login_url": full_login_url,
        },
    )
    send_email(
        subject=LOGIN_SUBJECT,
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )
