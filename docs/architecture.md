# 02. Architecture

This project is a Django-based web app centered around movie discovery, profile personalization, and lightweight recommendation logic.

## High-Level Structure

- `imdb_project/`: Django project configuration (`settings.py`, root URLs, WSGI/ASGI).
- `movie/`: Core application code (models, views, URLs, recommendation utilities, context processors, management command).
- `templates/`: HTML templates grouped by feature area.
- `static/`: CSS/JS/images used by templates.
- `scripts/`: one-off migration helper scripts (legacy utilities).

## Request Flow

1. User request enters via `imdb_project/urls.py`.
2. Root path delegates to `movie.urls`.
3. Matching function view in `movie/views.py` handles business logic.
4. View queries models in `movie/models.py`.
5. View renders template with context or returns JSON/partial template for HTMX interactions.

## Application Layers

### Presentation Layer

- Django templates in `templates/`
- Frontend interactions via JavaScript + HTMX partial updates
- Shared UI components in `templates/partials/`

### Domain/Data Layer

- `Movie`, `Category`, `Actor`, `MovieLinks`
- User-facing extensions with `Profile`, plus social interactions with `Comment`

### Recommendation Layer

- Runtime recommendations: `get_recommendations(movie_id)` in `movie/recommendations.py`
- Precompute task: `compute_all_recommendations()` and `update_recommendations` management command
- Uses TF-IDF and cosine similarity over title/category/cast/description features
- Cached in Django cache under keys like `rec_movie_<movie_id>`

### External Integrations

- TMDb helper functions in `movie/tmdb_utils.py`
- TVMaze API call in `views.tv_shows`

## Template and Static Asset Organization

- `templates/movies/`: listing/details/TV pages
- `templates/pages/`: profile/contact pages
- `templates/auth/`: login/signup
- `templates/partials/`: reusable snippets for HTMX replacement
- `static/css/`: modular styles (`base.css`, `layout.css`, page-level CSS)
- `static/js/`: custom scripts and vendor libraries

## Context Processors

Configured in `settings.py`:

- `slider_movie`: injects latest movie as `movie`
- `categories_processor`: injects category list as `categories_list`

This enables category navigation and slider content across multiple pages without repeating view logic.

## Security and Config Notes

- Environment-driven settings through `.env` (`python-dotenv`)
- `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` are read from environment
- In production, set `DEBUG=False` and use secure host/domain settings

## Known Technical Notes

- `requirements.txt` currently pins `Django==6.0.1`, while generated comments in settings reference older Django docs. Runtime behavior is controlled by installed package versions, not comment headers.
