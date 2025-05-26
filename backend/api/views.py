from rest_framework import viewsets

from .models import Movie, User, Comment, Rating
from .serializers import *

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.prefetch_related(
        "directors", "writers", "actors", "genres"
    ).all()
    serializer_class = MovieSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.select_related("user", "movie").all()
    serializer_class = CommentSerializer


class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rating.objects.select_related("user", "movie").all()
    serializer_class = RatingSerializer
