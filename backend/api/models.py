from django.db import models


# User Table
class UserTable(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    hashed_password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    state = models.CharField(max_length=50, default="active")

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.username} | {self.email}"


# Main Tables
class MoviesTable(models.Model):
    movie_name = models.CharField(max_length=255)
    release_year = models.IntegerField()
    age_rating = models.CharField(max_length=10)
    runtime = models.IntegerField()
    combined_rating = models.FloatField(default=0)
    poster = models.CharField(max_length=255)

    class Meta:
        unique_together = ("movie_name", "release_year", "runtime")

    def __str__(self):
        return f"{self.movie_name} | {self.release_year} | {self.runtime}"


class DirectorsTable(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


class WritersTable(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


class ActorsTable(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


class GenresTable(models.Model):
    genre_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.genre_name


class CommentsTable(models.Model):
    comment_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(MoviesTable, models.DO_NOTHING, db_column="movie_id")
    user_id = models.ForeignKey(UserTable, models.DO_NOTHING, db_column="user_id")
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment_id = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_column="parent_comment_id",
    )

    def __str__(self):
        return self.comment_text


class RatingsTable(models.Model):
    rating_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(MoviesTable, models.DO_NOTHING, db_column="movie_id")
    user_id = models.ForeignKey(UserTable, models.DO_NOTHING, db_column="user_id")
    rating_value = models.FloatField()
    review_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("id", "rating_value")

    def __str__(self):
        return f"{self.rating_value} | {self.user_id}"
