from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from core.utils import get_base_url
from core.celery import app
from bookmarks.models import Bookmark
from accounts.models import User


TEMPLATE = "emails/bookmark_login.txt"
SUBJECT = _("Please confirm your Aides-territoires alert")


@app.task
def send_alert_confirmation_email(user_email, bookmark_id):
    """Send a login email to the user.

    The email contains a token that can be used once to login.

    We use the default django token generator, that is usually used for
    password resets.
    """
    try:
        user = User.objects.get(email=user_email)
        bookmark = Bookmark.objects.get(id=bookmark_id)
    except (User.DoesNotExist, Bookmark.DoesNotExist):
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

    if bookmark.alert_frequency == Bookmark.FREQUENCIES.daily:
        frequency = _(
            "You will receive a daily email whenever new matching aids will be published."
        )  # noqa
    else:
        frequency = _(
            "You will receive a weekly email whenever new matching aids will be published."
        )  # noqa

    login_email_body = render_to_string(
        TEMPLATE,
        {
            "base_url": base_url,
            "user_name": user.full_name,
            "full_login_url": full_login_url,
            "bookmark": bookmark,
            "frequency": frequency,
        },
    )
    send_mail(
        SUBJECT,
        login_email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
