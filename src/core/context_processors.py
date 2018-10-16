def integration(request):
    """Add a context var if the GET `integration` variable is set."""
    integration = request.GET.get('integration', False)
    return {
        'integration': integration
    }
