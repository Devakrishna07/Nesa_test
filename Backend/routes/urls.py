from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.add_route,
        name='add_route'
    ),

    path(
        'search/',
        views.search_route,
        name='search_route'
    ),

    path(
        'longest/',
        views.longest_route_view,
        name='longest_route'
    ),

    path(
        'shortest/',
        views.shortest_route_view,
        name='shortest_route'
    ),
]