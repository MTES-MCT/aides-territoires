from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlencode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings

from core.utils import get_base_url
from core.celery import app
from accounts.models import User
from organizations.models import Organization
from emails.utils import send_email, send_email_with_template


LOGIN_SUBJECT = "Connexion à Aides-territoires"


@app.task
def send_connection_email(
    user_email,
    body_template="emails/login_token.txt",
    reset_password=False
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
        template_id = settings.SIB_WELCOME_MIXTE_EMAIL_TEMPLATE_ID
    elif user.is_contributor:
        template_id = settings.SIB_WELCOME_CONTRIBUTOR_EMAIL_TEMPLATE_ID
    elif user.is_beneficiary:
        template_id = settings.SIB_WELCOME_BENEFICIARY_EMAIL_TEMPLATE_ID

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
    invitation_author,
    organization_id,
    body_template="emails/invite_login_token.txt",
    collaborator_exist=False
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
    organization = Organization.objects.get(pk=organization_id)
    organization_name = organization.name

    if collaborator_exist is False:
        full_login_url = "{base_url}{url}".format(base_url=base_url, url=login_url)
    else:
        body_template="emails/invite_existent_user.txt",
        reverse_url = reverse("join_organization")
        full_login_url = f"{base_url}{reverse_url}"

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "invitation_author": invitation_author,
            "organization_name": organization_name,
            "user_name": user.full_name,
            "full_login_url": full_login_url,
        },
    )
    send_email(
        subject="invitation à collaborer sur Aides-territoires",
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )


@app.task
def send_reject_invitation_email(
    user_email,
    invited_name,
    organization_id,
    body_template="emails/reject_invitation.txt",
):
    """
    Send an email to the invitation author to inform him
    his invitation has been rejected.
    """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    base_url = get_base_url()
    organization = Organization.objects.get(pk=organization_id)
    organization_name = organization.name

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "invitation_author": user.full_name,
            "organization_name": organization_name,
            "invited_name": invited_name,
        },
    )
    send_email(
        subject="Rejet de votre invitation à collaborer sur Aides-territoires",
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )


@app.task
def send_accept_invitation_email(
    user_email,
    invited_name,
    organization_id,
    body_template="emails/accept_invitation.txt",
):
    """
    Send an email to the invitation author to inform him
    his invitation has been accepted.
    """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    base_url = get_base_url()
    organization = Organization.objects.get(pk=organization_id)
    organization_name = organization.name

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "invitation_author": user.full_name,
            "organization_name": organization_name,
            "invited_name": invited_name,
        },
    )
    send_email(
        subject="Votre invitation à collaborer sur Aides-territoires a été acceptée",
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )
