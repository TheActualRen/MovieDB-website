from django.contrib import admin
from .models import *

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("movie_name", "release_year", "combined_rating")
    search_fields = ("movie_name", )


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name", "last_name")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre_name",)
    search_fields = ("genre_name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created_at")
    search_fields = ("created_at",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "rating_value")
    list_filter = ("rating_value",)

    

admin.site.register(MovieDirector)
admin.site.register(MovieWriter)
admin.site.register(MovieActor)
admin.site.register(MovieGenre)

