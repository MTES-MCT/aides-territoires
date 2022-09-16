from django.urls import reverse
from django.conf import settings
from django.http import QueryDict

from core.utils import get_base_url
from core.celery import app
from aids.forms import AidSearchForm
from alerts.models import Alert
from emails.utils import send_email_with_template


@app.task
def send_alert_confirmation_email(user_email, alert_token):
    """Send an alert confirmation link to the user.

    The email contains a token that can be used to validate the
    email ownership.
    """
    try:
        alert = Alert.objects.get(token=alert_token)
    except (Alert.DoesNotExist):
        # In case we could not find any valid user with the given email
        # we don't raise any exception, because we can't give any hints
        # about whether or not any particular email has an account
        # on our site.
        return

    # Use the search form to parse the search querydict and
    # extract the perimeter
    querydict = QueryDict(alert.querystring)
    search_form = AidSearchForm(querydict)
    perimeter = ""
    if search_form.is_valid():
        perimeter = search_form.cleaned_data.get("perimeter") or ""
        perimeter = str(perimeter)

    base_url = get_base_url()
    alert_validation_link = reverse("alert_validate_view", args=[alert_token])
    alert_date = "{:%d/%m/%Y %H:%M:%S}".format(alert.date_created)

    if alert.alert_frequency == Alert.FREQUENCIES.daily:
        frequency = "quotidien"
    else:
        frequency = "hebdomadaire"

    data = {
        "URL_SITE": base_url,
        "FREQUENCE": frequency,
        "PERIMETRE": perimeter,
        "DATE_ALERTE": alert_date,
        "LIEN_VALIDATION": "{}{}".format(base_url, alert_validation_link),
    }

    send_email_with_template(
        recipient_list=[user_email],
        template_id=settings.SIB_ALERT_CONFIRMATION_EMAIL_TEMPLATE_ID,
        data=data,
        tags=["alerte_confirmation", settings.ENV_NAME],
        fail_silently=False,
    )
