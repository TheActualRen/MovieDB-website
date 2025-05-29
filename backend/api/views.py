from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import *
from .serializers import *


class UsersListCreate(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def delete(self, request, *args, **kwargs):
        Users.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    lookup_field = "pk"


class MoviesListCreate(generics.ListCreateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

    def delete(self, request, *args, **kwargs):
        Movies.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MoviesRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer
    lookup_field = "pk"


class DirectorsListCreate(generics.ListCreateAPIView):
    queryset = Directors.objects.all()
    serializer_class = DirectorsSerializer

    def delete(self, request, *args, **kwargs):
        Directors.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DirectorsRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Directors.objects.all()
    serializer_class = DirectorsSerializer
    lookup_field = "pk"


class WritersListCreate(generics.ListCreateAPIView):
    queryset = Writers.objects.all()
    serializer_class = WritersSerializer

    def delete(self, request, *args, **kwargs):
        Writers.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WritersRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Writers.objects.all()
    serializer_class = WritersSerializer
    lookup_field = "pk"


class ActorsListCreate(generics.ListCreateAPIView):
    queryset = Actors.objects.all()
    serializer_class = ActorsSerializer

    def delete(self, request, *args, **kwargs):
        Actors.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorsRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Actors.objects.all()
    serializer_class = ActorsSerializer
    lookup_field = "pk"


class GenresListCreate(generics.ListCreateAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

    def delete(self, request, *args, **kwargs):
        Genres.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenresRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = "pk"
