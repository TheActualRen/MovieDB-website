from django.urls import path

from . import views

urlpatterns = [
    path(
        "users/",
        views.UsersListCreate.as_view(),
        name="user-table-create",
    ),
    path(
        "users/<int:pk>/",
        views.UsersRetrieveUpdateDestroy.as_view(),
        name="update"
    ),
    path(
        "movies/",
        views.MoviesListCreate.as_view(),
        name="movies-table-create",
    ),
    path(
        "movies/<int:pk>/",
        views.MoviesRetrieveUpdateDestroy.as_view(),
        name="update",
    ),
    path(
        "directors/",
        views.DirectorsListCreate.as_view(),
        name="directors-table-create",
    ),
    path(
        "directors/<int:pk>/",
        views.DirectorsRetrieveUpdateDestroy.as_view(),
        name="update",
    ),
    path(
        "writers/",
        views.WritersListCreate.as_view(),
        name="writers-table-create",
    ),
    path(
        "writers/<int:pk>/",
        views.WritersRetrieveUpdateDestroy.as_view(),
        name="update",
    ),
    path("actors/", 
         views.ActorsListCreate.as_view(), 
         name="actors-table-create"
    ),
    path(
        "actors/<int:pk>/", 
        views.ActorsRetrieveUpdateDestroy.as_view(), 
        name="update"
    ),
    path(
        "genres/",
        views.GenresListCreate.as_view(),
        name="genres-table-create",
    ),
    path(
        "genres/<int:pk>/", views.GenresRetrieveUpdateDestroy.as_view(), name="update"
    ),
]
