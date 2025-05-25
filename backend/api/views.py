from rest_framework import viewsets

from .models import Movie, User, Comment, Rating
from .serializers import *

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related(
        "directors", "writers", "actors", "genres"
    ).all()
    serializer_class = MovieSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "movie").all()
    serializer_class = CommentSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.select_related("user", "movie").all()
    serializer_class = RatingSerializer
