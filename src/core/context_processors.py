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


def contributor_stats(request):
    """Injects contributor related stats."""

    context = {}
    if request.user.is_authenticated and request.user.is_contributor:
        aids = Aid.objects.drafts().filter(author=request.user)
        context['nb_draft_aids'] = aids.count()

    return context
