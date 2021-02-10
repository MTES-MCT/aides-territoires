from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings

from accounts.models import User
from core.celery import app
from emails.sib import send_mail_sib, send_mail_sib_with_template


LOGIN_SUBJECT = 'Connexion à Aides-territoires'


@app.task
def send_connection_email(user_email, body_template='emails/login_token.txt'):
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
    base_url = '{scheme}://{domain}'.format(
        scheme=scheme,
        domain=site.domain)
    full_login_url = '{base_url}{url}'.format(
        base_url=base_url,
        url=login_url)

    login_email_body = render_to_string(body_template, {
        'base_url': base_url,
        'user_name': user.full_name,
        'full_login_url': full_login_url})
    send_mail_sib(
        LOGIN_SUBJECT,
        login_email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False)


@app.task
def send_welcome_email(user_email):
    """Send a welcome email to the user."""
    user = User.objects.get(email=user_email)
    data = {
        'PRENOM': user.first_name,
        'NOM': user.last_name,
    }
    send_mail_sib_with_template(
        recipient_list=[user_email],
        template_id=settings.SIB_WELCOME_EMAIL_TEMPLATE_ID,
        data=data,
        fail_silently=True)
