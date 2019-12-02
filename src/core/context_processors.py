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
        manual_aids = Aid.objects.filter(is_imported=False)
        context['nb_draft_aids'] = manual_aids.drafts().count()
        context['nb_reviewable_aids'] = manual_aids.under_review().count()

        # Count the number of imported aids that are waiting
        # to be processed
        aids = Aid.objects \
            .filter(is_imported=True) \
            .filter(status__in=['draft', 'reviewable'])
        context['nb_waiting_imported_aids'] = aids.count()

    return context


def contributor_stats(request):
    """Injects contributor related stats."""

    context = {}
    if all((request.user.is_authenticated,
            request.user.is_contributor,
            not request.user.is_superuser)):
        aids = Aid.objects.drafts().filter(author=request.user)
        context['nb_draft_aids'] = aids.count()

    return context
