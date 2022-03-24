from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from core.utils import get_base_url
from core.celery import app
from accounts.models import User
from emails.utils import send_email, send_email_with_template


LOGIN_SUBJECT = 'Connexion à Aides-territoires'


@app.task
def send_project_deleted_email(user_email, project_name, eraser_name, body_template='emails/project_deleted.txt'):
    """Send a notification email to all organization's users.

    The email notify users that a project has been deleted.

    """
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    email_body = render_to_string(body_template, {
        'user_name': user.full_name,
        'eraser_name': eraser_name,
        'project_name': project_name})
    send_email(
        subject=LOGIN_SUBJECT,
        body=email_body,
        recipient_list=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        tags=['connexion', settings.ENV_NAME],
        fail_silently=False)
