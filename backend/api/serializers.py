from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username", "email"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["director_id", "first_name", "last_name"]

class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ["writer_id", "first_name", "last_name"]

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["actor_id", "first_name", "last_name"]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["genre_id", "genre_name"]

class MovieSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True, read_only=True)
    writers = WriterSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta: 
        model = Movie
        fields = "__all__"
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = "__all__"


