from django.db import models
from django.db.models.deletion import CASCADE

# User Table


class UsersTable(models.Model):
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
    user_id = models.ForeignKey(UsersTable, models.DO_NOTHING, db_column="user_id")
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
    user_id = models.ForeignKey(UsersTable, models.DO_NOTHING, db_column="user_id")
    rating_value = models.FloatField()
    review_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("id", "rating_value")

    def __str__(self):
        return f"{self.rating_value} | {self.user_id}"


# Junction Tables


class MovieDirectorsTable(models.Model):
    movie = models.ForeignKey(
        MoviesTable, on_delete=models.CASCADE, db_column="movie_id"
    )
    director = models.ForeignKey(
        DirectorsTable, on_delete=CASCADE, db_column="director_id"
    )

    class Meta:
        unique_together = ("movie", "director")
        db_table = "Movie_Directors"


class MovieWritersTable(models.Model):
    movie = models.ForeignKey(
        MoviesTable, on_delete=models.CASCADE, db_column="movie_id"
    )
    writer = models.ForeignKey(WritersTable, on_delete=CASCADE, db_column="writer_id")

    class Meta:
        unique_together = ("movie", "writer")
        db_table = "Movie_Writers"


class MovieActorsTable(models.Model):
    movie = models.ForeignKey(
        MoviesTable, on_delete=models.CASCADE, db_column="movie_id"
    )
    actor = models.ForeignKey(
        ActorsTable, on_delete=models.CASCADE, db_column="actor_id"
    )

    class Meta:
        unique_together = ("movie", "actor")
        db_table = "Movie_Actors"


class MovieGenres(models.Model):
    movie = models.ForeignKey(
        MoviesTable, on_delete=models.CASCADE, db_column="movie_id"
    )
    genre = models.ForeignKey(
        GenresTable, on_delete=models.CASCADE, db_column="genre_id"
    )

    class Meta:
        unique_together = ("movie", "genre")
        db_table = "Movie_Genres"
