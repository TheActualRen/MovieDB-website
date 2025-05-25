from django.db import models


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    username = models.TextField(unique=True)
    hashed_password = models.TextField()
    email = models.TextField(unique=True)
    state = models.TextField(default="active")

    class Meta:
        managed = False
        db_table = "Users"


class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.TextField()
    release_year = models.IntegerField()
    age_rating = models.TextField()
    runtime = models.IntegerField()
    combined_rating = models.FloatField()
    poster = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Movies"
        unique_together = (("movie_name", "release_year", "runtime"),)


class Directors(models.Model):
    director_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()

    class Meta:
        managed = False
        db_table = "Directors"
        unique_together = (("first_name", "last_name"),)


class MovieDirectors(models.Model):
    movie = models.ForeignKey(
        Movies, models.DO_NOTHING, db_column="movie_id", related_names="directors"
    )
    director = models.ForeignKey(
        Directors, models.DO_NOTHING, db_column="director_id", related_names="movies"
    )

    class Meta:
        managed = False
        db_table = "Movie_Directors"
        unique_together = (("movie", "director"),)


class Writers(models.Model):
    writer_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()

    class Meta:
        managed = False
        db_table = "Writers"
        unique_together = (("first_name", "last_name"),)


class MovieWriters(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    writer = models.ForeignKey(Writers, models.DO_NOTHING, db_column="writer_id")

    class Meta:
        managed = False
        db_table = "Movie_Writers"


class Actors(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()

    class Meta:
        managed = False
        db_table = "Actors"
        unique_together = (("first_name", "last_name"),)


class MovieActors(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    actor = models.ForeignKey(Actors, models.DO_NOTHING, db_column="actor_id")

    class Meta:
        managed = False
        db_table = "Movie_Actors"


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = "Genres"


class MovieGenres(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    genre = models.ForeignKey(Genres, models.DO_NOTHING, db_column="genre_id")

    class Meta:
        managed = False
        db_table = "Movie_Genres"
        unique_together = (("movie", "genre"),)


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column="user_id")
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    parent_comment = models.ForeignKey(
        "self", models.DO_NOTHING, db_column="parent_comment_id", null=True, blank=True
    )

    class Meta:
        managed = False
        db_table = "Comments"


class Ratings(models.Model):
    rating_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING, db_column="movie_id")
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column="user_id")
    rating_value = models.FloatField()
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "Ratings"
        unique_together = (("movie", "user"),)
