# 03. Data Model

This document describes the data model in `movie/models.py` and the relationships used by the app.

## Entity Overview

## `Category`

- Fields:
  - `name` (`CharField`)
  - `slug` (`SlugField`, auto-generated from name)
- Used as movie genres/tags via many-to-many relationship.

## `Actor`

- Fields:
  - `name` (`CharField`)
  - `slug` (`SlugField`, auto-generated from name)
- Connected to movies through many-to-many relationship (`Movie.cast`).

## `Movie`

- Core fields:
  - `title`, `description`
  - `image` (poster), `banner`
  - `language` (choice field)
  - `status` (choice field: recently added / most watched / top rated)
  - `year_of_production`, `views_count`, `movie_trailer`, `created`, `slug`
- Metadata fields:
  - `tmdb_id` (unique, optional)
  - `rating` (optional)
  - `featured` (boolean for homepage slider behavior)
- Relationships:
  - `category`: many-to-many to `Category`
  - `cast`: many-to-many to `Actor`

## `MovieLinks`

- Fields:
  - `movie` (`ForeignKey` to `Movie`)
  - `link_type` (download/watch)
  - `link` (`URLField`)
- Stores external watching/downloading links associated with a movie.

## `Profile`

- One-to-one extension of Django `User`.
- Fields:
  - `image` (profile image)
  - `bio`
  - `favorites` (many-to-many to `Movie`)
  - `watchlist` (many-to-many to `Movie`)
- Auto-created and auto-saved through `post_save` signals.

## `Comment`

- Fields:
  - `user` (`ForeignKey` to `User`)
  - `movie` (`ForeignKey` to `Movie`, reverse name `comments`)
  - `text`
  - `created_at`
- Represents user comments on movie detail pages.

## Relationship Diagram (Text)

- One `Movie` has many `MovieLinks`.
- One `Movie` has many `Comment`.
- One `User` has one `Profile`.
- One `Profile` has many favorite movies and many watchlist movies.
- One `Movie` has many categories and one category can belong to many movies.
- One `Movie` has many actors and one actor can belong to many movies.

## Signals

Two signals on `User` save keep `Profile` synchronized:

- `create_profile`: creates profile for new users.
- `save_profile`: saves existing profile or creates one if missing.

## Data Integrity Notes

- `Movie.tmdb_id` is unique to avoid duplicate TMDb movie records.
- Slugs are generated lazily on first save for `Category`, `Actor`, and `Movie`.
- Favorites and watchlist are deduplicated naturally by many-to-many semantics.
