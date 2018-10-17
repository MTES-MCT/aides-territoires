from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings

from core.celery import app
from accounts.models import User


LOGIN_SUBJECT = 'Connexion à Aides-Territoires'


@app.task
def send_connection_email(user_email):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    scheme = 'https'
    site = Site.objects.get_current()
    login_url = ''
    login_token = 'toto'
    full_login_url = '{scheme}://{domain}{url}/{token}'.format(
            scheme=scheme,
            domain=site.domain,
            url=login_url,
            token=login_token)

    login_email_body = render_to_string('emails/login_token.txt', {
        'user_name': user.full_name,
        'full_login_url': full_login_url})
    send_mail(
        LOGIN_SUBJECT,
        login_email_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False)
