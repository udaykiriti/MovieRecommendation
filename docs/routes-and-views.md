# 04. Routes and Views

This document maps URL routes to view behavior in `movie/urls.py` and `movie/views.py`.

## Root Routing

- Root URL config (`imdb_project/urls.py`) includes `movie.urls` at `/`.
- Admin is available at `/admin/`.

## Route Reference

## `GET /`

- View: `movies`
- Purpose: movie listing page
- Features:
  - Search via `q` query param
  - Pagination (12 per page)
  - Featured slider fallback if no featured movies
- Template: `movies/movie_list.html`

## `GET|POST /<int:_id>/`

- View: `movie_details`
- Purpose: show detail page for one movie
- Behavior:
  - Atomically increments `views_count`
  - Loads movie links and related recommendations
  - Accepts comment posting on `POST` for authenticated users
- Template: `movies/movie_details.html`

## `GET /<int:_id>/favorite/`

- View: `toggle_favorite`
- Purpose: add/remove movie from favorites
- Auth required: yes
- Response: `partials/favorite_icon.html` (HTMX-compatible partial)

## `GET /<int:_id>/watchlist/`

- View: `toggle_watchlist`
- Purpose: add/remove movie from watchlist
- Auth required: yes
- Response: `partials/watchlist_icon.html` (HTMX-compatible partial)

## `GET /category/<str:category>`

- View: `filter_by_category`
- Purpose: filter movie list by category name
- Template: `movies/movie_list.html`

## `GET /language/<str:language>`

- View: `filter_by_language`
- Purpose: filter movie list by language code/value
- Template: `movies/movie_list.html`

## `GET /tv-shows/`

- View: `tv_shows`
- Purpose: show top TV shows fetched from TVMaze API
- Template: `movies/tv_shows.html`

## `GET /search_results/?q=<text>`

- View: `search_results`
- Purpose: return compact search suggestions
- Response template: `partials/search_results.html`

## `GET /random_movie_data/`

- View: `random_movie_data`
- Purpose: provide JSON for slot-machine style "Surprise Me" feature
- Response: JSON with `reel` and `winner`

## `GET|POST /profile/`

- View: `profile_view`
- Purpose: authenticated user profile management
- Auth required: yes (`@login_required`)
- Template: `pages/profile.html`

## `GET /profile/<str:username>/`

- View: `public_profile`
- Purpose: public profile page for a specific username
- Template: `pages/public_profile.html`

## `GET /contact/`

- View: `contact`
- Template: `pages/contact.html`

## `GET|POST /signup/`

- View: `signup`
- Behavior: creates account with `UserCreationForm`, auto-login on success
- Template: `auth/signup.html`

## `GET|POST /login/`

- View: `login_view`
- Behavior: manual username/password authentication and session login
- Template: `auth/login.html`

## `GET /logout/`

- View: `logout_view`
- Behavior: logs user out and redirects to movie list

## API/Partial Response Patterns

- Full-page templates: movie list, details, profile, auth pages
- Partial template responses: favorite/watchlist/search snippets
- JSON responses: random movie data endpoint

This mixed pattern allows progressive enhancement with minimal frontend framework overhead.
