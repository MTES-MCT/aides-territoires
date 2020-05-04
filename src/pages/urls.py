from django.urls import path, include
from django.contrib.flatpages import views


urlpatterns = [
    path(
        'plateforme-aides-territoires/',
        views.flatpage,
        {'url': '/plateforme-aides-territoires/'},
        name='page_about_us'),
    path(
        'porteurs-aides/',
        views.flatpage,
        {'url': '/porteurs-aides/'},
        name='page_backers'),
    path(
        'aides-collectivites/',
        views.flatpage,
        {'url': '/aides-collectivites/'},
        name='page_communities'),
    path('', include('django.contrib.flatpages.urls')),
]
