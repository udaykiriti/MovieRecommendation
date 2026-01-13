from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path("", views.movies, name="movie"),
    path("<int:_id>/", views.movie_details, name="movie_details"),
    path("<int:_id>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("<int:_id>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("category/<str:category>", views.filter_by_category, name="filter_by_category"),
    path("language/<str:language>", views.filter_by_language, name="filter_by_language"),
    path("tv-shows/", views.tv_shows, name="tv_shows"),
    path("search_results/", views.search_results, name="search_results"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.public_profile, name="public_profile"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
