from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path("", views.movies, name="movie"),
    path("<int:_id>/", views.movie_details, name="movie_details"),
    path("<int:_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("category/<str:category>", views.filter_by_category, name="filter_by_category"),
    path("language/<str:language>", views.filter_by_language, name="filter_by_language"),
    path("tv-shows/", views.tv_shows, name="tv_shows"),
    path("profile/", views.profile_view, name="profile"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
