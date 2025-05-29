from rest_framework import serializers

from .models import *

# User Serializer


class UsersSerializer(serializers.ModelSerializer):
    hashed_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "hashed_password",
            "email",
            "state",
        ]


# Main Table Serializers


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = [
            "id",
            "movie_name",
            "release_year",
            "age_rating",
            "runtime",
            "combined_rating",
            "poster",
        ]


class DirectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = ["id", "first_name", "last_name"]


class WritersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writers
        fields = ["id", "first_name", "last_name"]


class ActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actors
        fields = ["id", "first_name", "last_name"]


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ["id", "genre_name"]


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            "id",
            "comment_text",
            "created_at",
            "parent_comment_id",
            "user_id",
            "movie_id",
        ]


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ["id", "rating_value", "review_text", "created_at"]


# Junction Table Serializers


class MovieDirectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDirectors
        fields = ["id", "movie", "director"]


class MovieWritersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieWriters
        fields = ["id", "movie", "writer"]


class MovieActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActors
        fields = ["id", "movie", "actor"]


class MovieGenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieGenres
        fields = ["id", "movie", "genre"]
