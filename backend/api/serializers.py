from rest_framework import serializers

from .models import *


class UsersTableSerializer(serializers.ModelSerializer):
    hashed_password = serializers.CharField(write_only=True)

    class Meta:
        model = UsersTable
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "hashed_password",
            "email",
            "state",
        ]


class MoviesTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesTable
        fields = [
            "id",
            "movie_name",
            "release_year",
            "age_rating",
            "runtime",
            "combined_rating",
            "poster",
        ]


class DirectorTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorsTable
        fields = ["id", "first_name", "last_name"]


class WritersTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritersTable
        fields = ["id", "first_name", "last_name"]


class ActorsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorsTable
        fields = ["id", "first_name", "last_name"]


class GenresTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenresTable
        fields = ["id", "genre_name"]


class CommentsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsTable
        fields = ["id", "comment_text", "created_at", "parent_comment_id"]


class RatingsTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingsTable
        fields = ["id", "rating_value", "review_text", "created_at"]
