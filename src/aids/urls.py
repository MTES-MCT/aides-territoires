from django.urls import path, include

from aids.views import (
    SearchView,
    ResultsView,
    ResultsReceiveView,
    AidDetailStatsView,
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
    AidProjectStatusView,
    AidExportView,
    AidDetailStatsExportView,
    AidDetailExportPdfView,
)

urlpatterns = [
    # Resultats & Plus de critères
    path("", SearchView.as_view(), name="search_view"),
    path("exporter-les-aides/", AidExportView.as_view(), name="aids_export_view"),
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
    ),
    path(
        "statistiques/<slug:slug>/",
        AidDetailStatsView.as_view(),
        name="aid_detail_stats_view",
    ),
    path(
        "exporter-aide-en-pdf/<slug:slug>/",
        AidDetailExportPdfView.as_view(),
        name="aid_detail_pdf_export_view",
    ),
    path(
        "exporter-les-stats/<slug:slug>/",
        AidDetailStatsExportView.as_view(),
        name="aid_detail_stats_export_view",
    ),
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
    path(
        "modifier-le-statut-de-l-aide/<int:pk>/",
        AidProjectStatusView.as_view(),
        name="aidproject_status_view",
    ),
]
