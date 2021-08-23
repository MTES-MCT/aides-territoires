try:
    # we use django.urls import as version detection as it will fail
    # on django 1.11 and thus we are safe to use
    # gettext_lazy instead of ugettext_lazy instead
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for src.
    """
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.ModelList(
            'Groupes et utilisateurs',
            deletable=False, draggable=False,
            models=('django.contrib.auth.*', 'accounts.*'),
        ))
        self.children.append(modules.ModelList(
            'Structures',
            deletable=False, draggable=False,
            models=('organizations.*',),
        ))
        self.children.append(modules.ModelList(
            'Aides',
            deletable=False, draggable=False,
            models=('aids.*',),
        ))
        self.children.append(modules.ModelList(
            'Aides - gestion avancées',
            deletable=False, draggable=False,
            models=(
                'geofr.*', 'backers.*', 'projects.*', 'programs.*',
                'categories.*',),
        ))
        self.children.append(modules.ModelList(
            'Alertes',
            deletable=False, draggable=False,
            models=('alerts.*',),
        ))
        self.children.append(modules.ModelList(
            'Contenu éditorial',
            deletable=False, draggable=False,
            models=('blog.*', 'pages.*', 'upload.*'),
        ))
        self.children.append(modules.ModelList(
            "Test d'eligibilité",
            deletable=False, draggable=False,
            models=('eligibility.*',),
        ))
        self.children.append(modules.Group(
            title="Pages Personnalisées",
            display="tabs",
            deletable=False, draggable=False,
            children=[
                modules.ModelList(
                    "Configuration",
                    models=(
                        'search.models.SearchPage',
                        'search.models.MinisiteTab',
                    )
                ),
                modules.ModelList(
                    "Espace Contributeur",
                    models=(
                        'search.models.SearchPageLite',
                        'search.models.MinisiteTabLite',
                    )
                ),
            ]
        ))
        self.children.append(modules.ModelList(
            'Statistiques',
            deletable=False, draggable=False,
            models=('stats.*',),
        ))
        self.children.append(modules.RecentActions(
            _('Recent Actions'), 5,
            deletable=False, draggable=False,
        ))
        self.children.append(modules.Group(
            title="Configuration Système",
            display="tabs",
            deletable=False, draggable=False,
            children=[
                modules.ModelList(
                    "Data et API",
                    models=(
                        'exporting.*', 'dataproviders.*',
                        'rest_framework.authtoken.*',),
                ),
                modules.ModelList(
                    "Config du site",
                    models=(
                        'django.contrib.sites.*',
                        'django_otp.plugins.otp_totp.*',
                    ),
                ),
                modules.ModelList(
                    "Tâches périodiques",
                    models=('django_celery_beat.*',),
                ),

            ]
        ))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for src.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
