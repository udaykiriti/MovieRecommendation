# 01. Local Setup

This guide shows how to run the project in local development, both directly with Python and with Docker.

## Prerequisites

- Python 3.11+ recommended
- `pip`
- Git
- Optional: Docker and Docker Compose

## 1. Clone and Enter the Repository

```bash
git clone <repository-url>
cd MovieRecommendation
```

## 2. Create and Activate a Virtual Environment

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Copy `.env.example` to `.env` and set values:

```bash
cp .env.example .env
```

Expected keys:

- `SECRET_KEY`: Django secret key
- `DEBUG`: `True` for local development, `False` for production
- `ALLOWED_HOSTS`: comma-separated host list (example: `127.0.0.1,localhost`)
- `TMDB_API_KEY`: required for TMDb-powered features

## 5. Run Migrations and Create Admin User

```bash
python manage.py migrate
python manage.py createsuperuser
```

## 6. Start the Development Server

```bash
python manage.py runserver
```

App URL: `http://127.0.0.1:8000/`
Admin URL: `http://127.0.0.1:8000/admin/`

## Docker Workflow

Build and start:

```bash
docker compose up --build
```

The container entrypoint runs:

1. `python manage.py migrate`
2. `python manage.py collectstatic --noinput`
3. `python manage.py runserver 0.0.0.0:8000`

Stop:

```bash
docker compose down
```

## Common Development Commands

```bash
# Create new migration files
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# Recompute recommendation cache
python manage.py update_recommendations
```

## Troubleshooting

- Static files not loading:
  - Confirm `DEBUG=True` locally and that `static/` exists.
- Image upload issues:
  - Confirm `MEDIA_ROOT` is writable and `MEDIA_URL` is configured.
- Recommendation errors:
  - Verify `pandas` and `scikit-learn` are installed from `requirements.txt`.
