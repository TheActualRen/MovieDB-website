from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    username = models.TextField(unique=True)
    hashed_password = models.TextField()
    email = models.TextField(unique=True)
    sstate = models.TextField(default="active")
    objects = models.Manager()

    def __str__(self):
        return f"Username: {self.username}. Name: {self.first_name} {self.last_name}"

    class Meta:
        managed = True
        db_table = "Users"


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    movie_name = models.TextField()
    release_year = models.IntegerField()
    age_rating = models.TextField()
    runtime = models.IntegerField()
    combined_rating = models.FloatField()
    poster = models.TextField(blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.movie_name} ({self.release_year})"

    class Meta:
        managed = True
        db_table = "Movies"
        unique_together = (("movie_name", "release_year", "runtime"),)
        ordering = ["movie_id"]


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return f"Director Name: {self.first_name} {self.last_name}"

    class Meta:
        managed = True
        db_table = "Directors"
        unique_together = (("first_name", "last_name"),)
        ordering = ["director_id"]


class MovieDirector(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        Movie, models.DO_NOTHING, db_column="movie_id", related_name="directors"
    )
    director = models.ForeignKey(
        Director, models.DO_NOTHING, db_column="director_id", related_name="movies"
    )

    class Meta:
        managed = True
        db_table = "Movie_Directors"
        unique_together = (("movie", "director"),)


class Writer(models.Model):
    writer_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return f"Writer Name: {self.first_name} {self.last_name}"

    class Meta:
        managed = True
        db_table = "Writers"
        unique_together = (("first_name", "last_name"),)
        ordering = ["writer_id"]


class MovieWriter(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        Movie, models.DO_NOTHING, db_column="movie_id", related_name="writers"
    )
    writer = models.ForeignKey(
        Writer, models.DO_NOTHING, db_column="writer_id", related_name="movies"
    )

    class Meta:
        managed = True
        db_table = "Movie_Writers"
        unique_together = (("movie", "writer"),)


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return f"Actor Name: {self.first_name} {self.last_name}"

    class Meta:
        managed = True
        db_table = "Actors"
        unique_together = (("first_name", "last_name"),)
        ordering = ["actor_id"]


class MovieActor(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        Movie, models.DO_NOTHING, db_column="movie_id", related_name="actors"
    )
    actor = models.ForeignKey(
        Actor, models.DO_NOTHING, db_column="actor_id", related_name="movies"
    )

    class Meta:
        managed = True
        db_table = "Movie_Actors"


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.TextField(unique=True)
    objects = models.Manager()

    def __str__(self):
        return f"Genre: {self.genre_name}"

    class Meta:
        managed = True
        db_table = "Genres"
        ordering = ["genre_id"]


class MovieGenre(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(
        Movie, models.DO_NOTHING, db_column="movie_id", related_name="genres"
    )
    genre = models.ForeignKey(
        Genre, models.DO_NOTHING, db_column="genre_id", related_name="movies"
    )

    class Meta:
        managed = True
        db_table = "Movie_Genres"
        unique_together = (("movie", "genre"),)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING, db_column="movie_id", null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column="user_id", null=True)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    parent_comment = models.ForeignKey(
        "self", models.DO_NOTHING, db_column="parent_comment_id", null=True, blank=True
    )

    def __str__(self):
        return f"Movie: {self.movie} User: {self.user} Comment: {self.comment_text}"

    class Meta:
        managed = True
        db_table = "Comments"
        ordering = ["comment_id"]


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING, db_column="movie_id", null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column="user_id", null=True)
    rating_value = models.FloatField()
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f"Movie: {self.movie} User: {self.user} Rating: {self.rating_value}"

    class Meta:
        managed = True
        db_table = "Ratings"
        unique_together = (("movie", "user"),)
        ordering = ["rating_id"]
