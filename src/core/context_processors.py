from aids.models import Aid


def integration(request):
    """Add a context var if the GET `integration` variable is set."""
    integration = request.GET.get('integration', False)
    return {
        'integration': integration
    }


def admin_stats(request):
    """Injects administrator specific data."""

    context = {}
    if request.user.is_superuser:
        aids = Aid.objects.under_review()
        context['nb_aids_under_review'] = aids.count()

    return context
