from django.urls import path

from . import views

urlpatterns = [
    path(
        "Movies/",
        views.MoviesTableListCreate.as_view(),
        name="movies-table-create",
    ),
    path(
        "Movies/<int:pk>/",
        views.MoviesTableRetrieveUpdateDestroy.as_view(),
        name="update",
    ),
]
