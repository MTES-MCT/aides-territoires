from django.template.loader import render_to_string
from django.conf import settings

from core.celery import app
from accounts.models import User
from emails.utils import send_email


@app.task
def send_project_deleted_email(user_email, project_name, eraser_name):
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

    if not settings.SIB_DELETE_PROJECT_EMAIL_ENABLED:
        return

    data = {
        'USER_NAME': user.full_name,
        'ERASER_NAME': eraser_name,
        'PROJECT_NAME': project_name
    }
    send_email_with_template(
        recipient_list=[user_email],
        template_id=settings.SIB_DELETE_PROJECT_EMAIL_TEMPLATE_ID,
        data=data,
        tags=['suppression de projet', settings.ENV_NAME],
        fail_silently=True)
