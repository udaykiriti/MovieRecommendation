# 05. Operations and Maintenance

This document covers recurring maintenance tasks, background operations, and practical production notes.

## Management Commands

## Update Recommendation Cache

Command:

```bash
python manage.py update_recommendations
```

What it does:

1. Builds combined text features for all movies (`title`, `category`, `cast`, `description`).
2. Runs TF-IDF vectorization + cosine similarity.
3. Caches top recommendations per movie with keys like `rec_movie_<movie_id>`.

When to run:

- After significant movie catalog updates
- As a scheduled task (for example daily)

## Database Tasks

## Apply migrations

```bash
python manage.py migrate
```

## Create new migrations after model updates

```bash
python manage.py makemigrations
python manage.py migrate
```

## Static and Media Handling

- Static files are served from `static/` in development.
- Media files are stored in `media/` (`MEDIA_ROOT`).
- Docker entrypoint runs `collectstatic --noinput` at container startup.

For production deployment, use:

- A dedicated web server/CDN for static files
- Persistent storage for media uploads

## Environment Configuration Checklist

- `SECRET_KEY` is set and not the fallback default
- `DEBUG=False` in production
- `ALLOWED_HOSTS` contains actual domain(s)
- `TMDB_API_KEY` is configured if using TMDb integration

## External Service Dependencies

- TVMaze API: used by `/tv-shows/`
- TMDb API: helper functions for import/search workflows

Add request timeouts and retries if you harden this for production.

## Legacy Script Notes (`scripts/`)

- `scripts/migrate_genres.py`
- `scripts/migrate_actors.py`

These appear to reference older field names (`genres`, `new_cast`, string-like `cast`) from previous schema versions. Treat them as historical utilities, not safe default scripts for the current schema.

## Suggested Operational Improvements

1. Add periodic job scheduling for `update_recommendations`.
2. Configure a real cache backend (Redis/Memcached) instead of local-memory fallback.
3. Add logging around external API failures and recommendation updates.
4. Add test coverage for routes returning partials/JSON and for profile/favorites/watchlist flows.
