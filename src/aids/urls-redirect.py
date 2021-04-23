from django.urls import path, include
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from aids.views import (AidDetailView)

urlpatterns = [
    path('<slug:slug>/', RedirectView.as_view(url=reverse_lazy('aid_detail_view', args=['<slug:slug>']), permanent=False)),
]
