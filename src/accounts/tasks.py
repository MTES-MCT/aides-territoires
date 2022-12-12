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
from aids.models import Aid
from projects.models import Project
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
    collaborator_exist=False,
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
        body_template = ("emails/invite_existent_user.txt",)
        reverse_url = reverse("join_organization")
        full_login_url = f"{base_url}{reverse_url}"

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "invitation_author": invitation_author,
            "organization_name": organization_name,
            "current_organization_name": user.organization_set.first().name,
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


@app.task
def send_leave_organization_email(
    former_collaborator_email,
    user_name,
    former_organization_id,
    body_template="emails/leave_organization.txt",
):
    """
    Send an email to the former collaborator to inform him
    the user left the organization.
    """
    try:
        user = User.objects.get(email=former_collaborator_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    base_url = get_base_url()
    organization = Organization.objects.get(pk=former_organization_id)
    organization_name = organization.name

    login_email_body = render_to_string(
        body_template,
        {
            "base_url": base_url,
            "former_collaborator": user.full_name,
            "organization_name": organization_name,
            "user_name": user_name,
        },
    )
    send_email(
        subject="Un collaborateur a quitté votre structure sur Aides-territoires",
        body=login_email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=["connexion", settings.ENV_NAME],
        fail_silently=False,
    )


@app.task
def send_new_suggested_aid_notification_email(
    project_author_email,
    suggester_user_email,
    suggester_organization_name,
    project_id,
    suggested_aid_id,
    body_template="emails/new_suggested_aid.txt",
):
    """
    Send an email to the project's authors to inform them
    a new aid was suggested for the project.
    """
    try:
        project_author = User.objects.get(email=project_author_email)
        suggester_user = User.objects.get(email=suggester_user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    suggested_aid = Aid.objects.get(id=suggested_aid_id)
    suggested_aid_financer_name = suggested_aid.financers.first().name
    if suggested_aid.recurrence == "oneoff" or suggested_aid.recurrence == "recurring":
        suggested_aid_recurrence_string = ""
        if suggested_aid.submission_deadline:
            submission_deadline = suggested_aid.submission_deadline.strftime("%d/%m/%y")
            suggested_aid_recurrence_string = (
                f"clôture de l'aide le {submission_deadline}"
            )
    else:
        suggested_aid_recurrence_string = suggested_aid.get_recurrence_display()
    project = Project.objects.get(id=project_id)
    base_url = get_base_url()
    reverse_account_url = reverse("user_dashboard")
    full_account_url = f"{base_url}{reverse_account_url}"
    reverse_project_url = reverse(
        "project_detail_view", args=[project.id, project.slug]
    )
    full_project_url = f"{base_url}{reverse_project_url}"

    if settings.SIB_SUGGESTED_AID_EMAIL_ENABLED:
        data = {
            "PROJECT_AUTHOR_NAME": project_author.full_name,
            "SUGGESTER_USER_NAME": suggester_user.full_name,
            "SUGGESTER_ORGANIZATION_NAME": suggester_organization_name,
            "PROJECT_NAME": project.name,
            "SUGGESTED_AID_NAME": suggested_aid.name,
            "SUGGESTED_AID_FINANCER_NAME": suggested_aid_financer_name,
            "SUGGESTED_AID_RECURRENCE": suggested_aid_recurrence_string,
            "FULL_ACCOUNT_URL": full_account_url,
            "FULL_PROJECT_URL": full_project_url,
        }

        template_id = settings.SIB_NEW_SUGGESTED_AID_TEMPLATE_ID

        send_email_with_template(
            recipient_list=[project_author.email],
            template_id=template_id,
            data=data,
            tags=["aide suggérée", settings.ENV_NAME],
            fail_silently=True,
        )

    else:
        login_email_body = render_to_string(
            body_template,
            {
                "project_author_name": project_author.full_name,
                "suggester_user_name": suggester_user.full_name,
                "suggester_organization_name": suggester_organization_name,
                "project_name": project.name,
                "suggested_aid_name": suggested_aid.name,
                "suggested_aid_financer_name": suggested_aid_financer_name,
                "suggested_aid_recurrence": suggested_aid_recurrence_string,
                "full_account_url": full_account_url,
                "full_project_url": full_project_url,
            },
        )
        send_email(
            subject="Une aide vous a été suggérée pour votre projet",
            body=login_email_body,
            recipient_list=[project_author.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            tags=["aide suggérée", settings.ENV_NAME],
            fail_silently=False,
        )


@app.task
def send_suggested_aid_accepted_notification_email(
    project_author_organization_name,
    suggester_user_email,
    project_id,
    suggested_aid_id,
    body_template="emails/suggested_aid_accepted.txt",
):
    """
    Send an email to the aid's suggester to inform him
    the aid was accepted for the project.
    """
    try:
        suggester_user = User.objects.get(email=suggester_user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    suggested_aid = Aid.objects.get(id=suggested_aid_id)
    suggested_aid_financer_name = suggested_aid.financers.first().name
    project = Project.objects.get(id=project_id)
    favorite_project = False
    if project in suggester_user.beneficiary_organization.favorite_projects.all():
        favorite_project = True
    base_url = get_base_url()
    reverse_public_project_url = reverse(
        "public_project_detail_view", args=[project.id, project.slug]
    )
    full_project_url = f"{base_url}{reverse_public_project_url}"
    reverse_public_projects_list_url = reverse("public_project_list_view")
    full_public_projects_list_url = f"{base_url}{reverse_public_projects_list_url}"

    if settings.SIB_SUGGESTED_AID_EMAIL_ENABLED:
        data = {
            "PROJECT_AUTHOR_ORGANIZATION_NAME": project_author_organization_name,
            "SUGGESTER_USER_NAME": suggester_user.full_name,
            "PROJECT_NAME": project.name,
            "SUGGESTED_AID_NAME": suggested_aid.name,
            "SUGGESTED_AID_FINANCER_NAME": suggested_aid_financer_name,
            "FULL_PROJECT_URL": full_project_url,
            "FULL_PUBLIC_PROJECTS_LIST_URL": full_public_projects_list_url,
            "FAVORITE_PROJECT": favorite_project,
        }

        template_id = settings.SIB_SUGGESTED_AID_ACCEPTED_TEMPLATE_ID

        send_email_with_template(
            recipient_list=[suggester_user.email],
            template_id=template_id,
            data=data,
            tags=["aide suggérée acceptée", settings.ENV_NAME],
            fail_silently=True,
        )

    else:
        login_email_body = render_to_string(
            body_template,
            {
                "project_author_organization_name": project_author_organization_name,
                "suggester_user_name": suggester_user.full_name,
                "project_name": project.name,
                "suggested_aid_name": suggested_aid.name,
                "suggested_aid_financer_name": suggested_aid_financer_name,
                "full_project_url": full_project_url,
                "full_public_projects_list_url": full_public_projects_list_url,
                "favorite_project": favorite_project,
            },
        )
        send_email(
            subject="L’aide que vous avez suggérée a plu !",
            body=login_email_body,
            recipient_list=[suggester_user.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            tags=["aide suggérée acceptée", settings.ENV_NAME],
            fail_silently=False,
        )


@app.task
def send_suggested_aid_denied_notification_email(
    project_author_organization_name,
    suggester_user_email,
    project_id,
    suggested_aid_id,
    body_template="emails/suggested_aid_denied.txt",
):
    """
    Send an email to the aid's suggester to inform him
    the aid was denied for the project.
    """
    try:
        suggester_user = User.objects.get(email=suggester_user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    suggested_aid = Aid.objects.get(id=suggested_aid_id)
    suggested_aid_financer_name = suggested_aid.financers.first().name
    project = Project.objects.get(id=project_id)
    favorite_project = False
    if project in suggester_user.beneficiary_organization.favorite_projects.all():
        favorite_project = True
    base_url = get_base_url()
    reverse_public_project_url = reverse(
        "public_project_detail_view", args=[project.id, project.slug]
    )
    full_project_url = f"{base_url}{reverse_public_project_url}"
    reverse_public_projects_list_url = reverse("public_project_list_view")
    full_public_projects_list_url = f"{base_url}{reverse_public_projects_list_url}"

    if settings.SIB_SUGGESTED_AID_EMAIL_ENABLED:
        data = {
            "PROJECT_AUTHOR_ORGANIZATION_NAME": project_author_organization_name,
            "SUGGESTER_USER_NAME": suggester_user.full_name,
            "PROJECT_NAME": project.name,
            "SUGGESTED_AID_NAME": suggested_aid.name,
            "SUGGESTED_AID_FINANCER_NAME": suggested_aid_financer_name,
            "FULL_PROJECT_URL": full_project_url,
            "FULL_PUBLIC_PROJECTS_LIST_URL": full_public_projects_list_url,
            "FAVORITE_PROJECT": favorite_project,
        }

        template_id = settings.SIB_SUGGESTED_AID_DENIED_TEMPLATE_ID

        send_email_with_template(
            recipient_list=[suggester_user.email],
            template_id=template_id,
            data=data,
            tags=["aide suggérée rejetée", settings.ENV_NAME],
            fail_silently=True,
        )

    else:
        login_email_body = render_to_string(
            body_template,
            {
                "project_author_organization_name": project_author_organization_name,
                "suggester_user_name": suggester_user.full_name,
                "project_name": project.name,
                "suggested_aid_name": suggested_aid.name,
                "suggested_aid_financer_name": suggested_aid_financer_name,
                "full_project_url": full_project_url,
                "full_public_projects_list_url": full_public_projects_list_url,
                "favorite_project": favorite_project,
            },
        )
        send_email(
            subject="Des nouvelles de l’aide que vous avez suggérée",
            body=login_email_body,
            recipient_list=[suggester_user.email],
            from_email=settings.DEFAULT_FROM_EMAIL,
            tags=["aide suggérée rejetée", settings.ENV_NAME],
            fail_silently=False,
        )
