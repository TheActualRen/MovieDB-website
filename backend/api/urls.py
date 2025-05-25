from django.urls import include, path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"movies", views.MovieViewSet)
router.register(r"users", views.UserViewSet)
router.register(r"comments", views.CommentViewSet)
router.register(r"ratings", views.RatingViewSet)

urlpatterns = [path("", include(router.urls))]
