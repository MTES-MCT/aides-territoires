from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings

from core.celery import app
from accounts.models import User


LOGIN_SUBJECT = 'Connexion à Aides-Territoires'


@app.task
def send_connection_email(user_email):
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

    site = Site.objects.get_current()
    scheme = 'https'
    user_uid = urlsafe_base64_encode(force_bytes(user.pk))
    login_token = default_token_generator.make_token(user)
    login_url = reverse('token_login', args=[user_uid, login_token])
    full_login_url = '{scheme}://{domain}{url}'.format(
            scheme=scheme,
            domain=site.domain,
            url=login_url)

    login_email_body = render_to_string('emails/login_token.txt', {
        'user_name': user.full_name,
        'full_login_url': full_login_url})
    send_mail(
        LOGIN_SUBJECT,
        login_email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False)
