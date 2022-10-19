from django.conf import settings
from aids.models import Aid


def integration(request):
    """Add a context var if the GET `integration` variable is set."""
    integration = request.GET.get("integration", False)
    return {"integration": integration}


def contact_data(request):
    return {
        "contact_email": settings.CONTACT_EMAIL,
        "contact_phone": settings.CONTACT_PHONE,
    }


def admin_environment(request):
    """Injects administrator-specific environment info"""
    env_name = settings.ENV_NAME
    color = "white"

    if settings.ENV_NAME == "production":
        background_color = "#3a3188"
    elif settings.ENV_NAME == "staging":
        background_color = "#009099"
    else:
        background_color = "#00A95F"

    return {
        "ENV_NAME": env_name,
        "ENV_BACKGROUND_COLOR": background_color,
        "ENV_COLOR": color,
    }


def admin_stats(request):
    """Injects administrator specific data.

    Note: this adds three queries to every single page for admin users.

    Maybe one day, caching could be of some use, but it's premature at this
    time.
    """

    context = {}
    if request.user.is_superuser:
        manual_aids = Aid.objects.filter(is_imported=False)
        context["nb_draft_aids"] = manual_aids.drafts().count()
        context["nb_reviewable_aids"] = manual_aids.under_review().count()

        # Count the number of imported aids that are waiting
        # to be processed
        aids = Aid.objects.filter(is_imported=True).filter(
            status__in=["draft", "reviewable"]
        )
        context["nb_waiting_imported_aids"] = aids.count()

    return context


def contributor_stats(request):
    """Injects contributor related stats."""

    context = {}
    if (
        request.user.is_authenticated
        and request.user.is_contributor
        and not request.user.is_superuser
    ):
        aids = Aid.objects.drafts().filter(author=request.user)
        context["nb_draft_aids"] = aids.count()

    return context
