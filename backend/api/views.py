from django.shortcuts import render
from .models import *
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *


class MoviesTableListCreate(generics.ListCreateAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

    # def get(self):
    #     pass
    #
    def delete(self, request, *args, **kwargs):
        Movies.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MoviesTableRetrieveUpdateDestroy(generics.RetrieveDestroyAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer
    lookup_field = "pk"


     
