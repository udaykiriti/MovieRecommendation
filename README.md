# GrandLine Cinema

A Django-based movie recommendation web app with a modern browsing UI, user profiles, favorites/watchlist, comments, and cached content-based recommendations.

## Features

- Movie catalog browsing with pagination
- Movie detail pages with comments and related recommendations
- Favorites and watchlist toggles (HTMX partial updates)
- Search suggestions and filtering by category/language
- Random "Surprise Me" movie endpoint
- User auth (signup/login/logout) and profile pages
- TV shows page powered by TVMaze API

## Tech Stack

- Python + Django (`Django==6.0.1` in `requirements.txt`)
- SQLite by default
- HTML/CSS/JavaScript templates
- `requests` for external APIs
- `pandas` + `scikit-learn` for recommendation precomputation

## Quick Start (Local)

```bash
git clone <repository-url>
cd MovieRecommendation
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

> [!TIP]
> After adding or bulk-importing movies, run `python manage.py update_recommendations` to refresh cached related-movie results.

## Environment Variables

Create `.env` (based on `.env.example`) with:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `TMDB_API_KEY`

> [!NOTE]
> Use `DEBUG=True` only in local development, and always set a strong `SECRET_KEY` for any shared/staging/production environment.

## Docker

```bash
docker compose up --build
```

This runs migrations, collects static files, and starts Django on `0.0.0.0:8000`.

> [!TIP]
> If you change dependencies or Docker build steps, rebuild with `docker compose up --build` again.

## Useful Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Recompute recommendation cache
python manage.py update_recommendations
```

> [!NOTE]
> Favorites/watchlist actions require authentication and are returned as HTMX-friendly partial responses.

## Project Layout

- `imdb_project/`: Django project settings and root URL config
- `movie/`: app models, views, urls, recommendation logic, management commands
- `templates/`: page templates and reusable partials
- `static/`: CSS, JavaScript, images
- `docs/`: detailed technical documentation

> [!NOTE]
> Scripts under `scripts/` are legacy migration helpers for older schema versions; review before reuse.

## Documentation

Detailed docs are in [docs/README.md](docs/README.md):

- Local setup
- Architecture
- Data model
- Routes and views
- Operations and maintenance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests where applicable
4. Open a pull request
