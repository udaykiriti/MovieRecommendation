from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path("", views.movies, name="movie"),
    path("<int:_id>/", views.movie_details, name="movie_details"),
    path("category/<str:category>", views.filter_by_category, name="filter_by_category"),
    path("language/<str:language>", views.filter_by_language, name="filter_by_language"),
    
]
