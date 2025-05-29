from django.db import models
from django.db.models.deletion import CASCADE

# User Table


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    hashed_password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    state = models.CharField(max_length=50, default="active")

    class Meta:
        db_table = "Users"
        managed = False

    def __str__(self):
        return f"{self.first_name} | {self.last_name} | {self.username} | {self.email}"


# Main Tables


class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=255)
    release_year = models.IntegerField()
    age_rating = models.CharField(max_length=10)
    runtime = models.IntegerField()
    combined_rating = models.FloatField(default=0)
    poster = models.CharField(max_length=255)

    class Meta:
        db_table = "Movies"
        managed = False
        unique_together = ("movie_name", "release_year", "runtime")

    def __str__(self):
        return f"{self.movie_name} | {self.release_year} | {self.runtime}"


class Directors(models.Model):
    director_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        db_table = "Directors"
        managed = False
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


class Writers(models.Model):
    writer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        db_table = "Writers"
        managed = False
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


class Actors(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        db_table = "Actors"
        managed = False
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} | {self.last_name}"


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "Genres"
        managed = False

    def __str__(self):
        return self.genre_name


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    user_id = models.ForeignKey(Users, models.DO_NOTHING, db_column="user_id")
    comment_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment_id = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        db_column="parent_comment_id",
    )

    class Meta:
        db_table = "Comments"
        managed = False

    def __str__(self):
        return self.comment_text


class Ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    user_id = models.ForeignKey(Users, models.DO_NOTHING, db_column="user_id")
    rating_value = models.FloatField()
    review_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Ratings"
        managed = False
        unique_together = ("movie_id", "user_id")

    def __str__(self):
        return f"{self.rating_value} | {self.user_id}"


# Junction Tables


class MovieDirectors(models.Model):
    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, db_column="movie_id", to_field="movie_id"
    )
    director = models.ForeignKey(
        Directors, on_delete=CASCADE, db_column="director_id", to_field="director_id"
    )

    class Meta:
        unique_together = ("movie", "director")
        db_table = "Movie_Directors"
        managed = False


class MovieWriters(models.Model):
    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, db_column="movie_id", to_field="movie_id"
    )
    writer = models.ForeignKey(
        Writers, on_delete=CASCADE, db_column="writer_id", to_field="writer_id"
    )

    class Meta:
        unique_together = ("movie", "writer")
        db_table = "Movie_Writers"
        managed = False


class MovieActors(models.Model):
    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, db_column="movie_id", to_field="movie_id"
    )
    actor = models.ForeignKey(
        Actors, on_delete=models.CASCADE, db_column="actor_id", to_field="actor_id"
    )

    class Meta:
        unique_together = ("movie", "actor")
        db_table = "Movie_Actors"
        managed = False


class MovieGenres(models.Model):
    movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, db_column="movie_id", to_field="movie_id"
    )
    genre = models.ForeignKey(
        Genres, on_delete=models.CASCADE, db_column="genre_id", to_field="genre_id"
    )

    class Meta:
        unique_together = ("movie", "genre")
        db_table = "Movie_Genres"
        managed = False
