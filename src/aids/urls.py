from django.urls import path, include
from django.utils.translation import ugettext_lazy as _

from aids.views import (SearchView, ResultsView, ResultsReceiveView,
                        AidDetailView, AidCreateView, AidDraftListView,
                        AidEditView, AidStatusUpdate, AidDeleteView)

urlpatterns = [
    path('', SearchView.as_view(), name='search_view'),
    path(_('results/'), ResultsView.as_view(), name='results_view'),
    path(_('results/receive/'), ResultsReceiveView.as_view(),
         name='results_receive_view'),
    path(_('publish/'), AidCreateView.as_view(), name='aid_create_view'),
    path(_('published/'), include([
        path('', AidDraftListView.as_view(), name='aid_draft_list_view'),
        path('<slug:slug>/', AidEditView.as_view(), name='aid_edit_view'),
        path(_('<slug:slug>/status/'), AidStatusUpdate.as_view(),
             name='aid_status_update_view'),
        path(_('<slug:slug>/delete/'), AidDeleteView.as_view(),
             name='aid_delete_view'),
    ])),

    path('<slug:slug>/', AidDetailView.as_view(), name='aid_detail_view'),
]
