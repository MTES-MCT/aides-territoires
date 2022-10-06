from django.urls import path, include

from aids.views import (
    SearchView,
    AdvancedSearchView,
    ResultsView,
    ResultsReceiveView,
    AidDetailView,
    AidCreateView,
    AidDraftListView,
    AidEditView,
    AidDeleteView,
    GenericToLocalAidView,
    AidMatchProjectView,
    AidUnmatchProjectView,
    SuggestAidMatchProjectView,
    SuggestedAidUnmatchProjectView,
)

urlpatterns = [
    # Resultats & Plus de critères
    path("", SearchView.as_view(), name="search_view"),
    path("recherche/", AdvancedSearchView.as_view(), name="advanced_search_view"),
    path("resultats/", ResultsView.as_view(), name="results_view"),
    path(
        "resultats/recevoir/", ResultsReceiveView.as_view(), name="results_receive_view"
    ),
    # Espace contributeur
    path("publier/", AidCreateView.as_view(), name="aid_create_view"),
    path(
        "publications/",
        include(
            [
                path("", AidDraftListView.as_view(), name="aid_draft_list_view"),
                path("<slug:slug>/", AidEditView.as_view(), name="aid_edit_view"),
                path(
                    "<slug:slug>/supprimer/",
                    AidDeleteView.as_view(),
                    name="aid_delete_view",
                ),
            ]
        ),
    ),
    path(
        "dupliquer/<slug:slug>/",
        GenericToLocalAidView.as_view(),
        name="aid_generic_to_local_view",
    ),  # noqa
    # Aid détails
    path(
        "<slug:slug>/",
        include([path("", AidDetailView.as_view(), name="aid_detail_view")]),
    ),
    path(
        "associer-des-projets/<slug:slug>/",
        AidMatchProjectView.as_view(),
        name="aid_match_project_view",
    ),
    path(
        "déassocier-un-projet/<slug:slug>/",
        AidUnmatchProjectView.as_view(),
        name="aid_unmatch_project_view",
    ),
    path(
        "suggérer-une-aide/",
        SuggestAidMatchProjectView.as_view(),
        name="suggest_aid_view",
    ),
    path(
        "rejeter-une-aide-suggérée/<slug:slug>/",
        SuggestedAidUnmatchProjectView.as_view(),
        name="reject_suggested_aid_view",
    ),
]
