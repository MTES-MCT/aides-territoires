from django.urls import path

from programs.views import ProgramList, ProgramDetail


urlpatterns = [
    path("", ProgramList.as_view(), name="program_list"),
    path("<slug:slug>/", ProgramDetail.as_view(), name="program_detail"),
]
