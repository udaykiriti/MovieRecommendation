# Movie Recommendation System

A web-based movie recommendation and listing platform built with Django. This application allows users to browse movies, search by title, filter by category or language, and view detailed information including cast, trailers, and download links.

## Features

*   **Movie Listing:** Browse a paginated list of movies with their posters.
*   **Search:** Search for movies by title.
*   **Filters:** Filter movies by:
    *   **Category:** Action, Drama, Comedy, Romance.
    *   **Language:** English, German.
*   **Detailed View:** View comprehensive movie details:
    *   Description, Release Year, Cast.
    *   Watch Trailer.
    *   Download/Watch Links.
    *   Related Movies suggestions.
*   **Analytics:** Tracks view counts for each movie.
*   **Responsive Design:** Includes a slider for featured movies and a responsive grid layout.

## Tech Stack

*   **Backend:** Python 3, Django 3.2+
*   **Database:** SQLite (Default)
*   **Frontend:** HTML, CSS, JavaScript (jQuery, Swiper.js)

## Installation & Setup

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MovieRecommendation
```

### 2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install Django and Pillow (for image handling).

```bash
pip install django pillow
```
*(If a `requirements.txt` file is present, you can run `pip install -r requirements.txt` instead)*

### 4. Apply Database Migrations

Set up the SQLite database.

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)

To access the Django admin panel to add movies:

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Structure

*   **`imdb_project/`**: Main project configuration settings and URLs.
*   **`movie/`**: The core application handling models, views, and templates.
    *   `models.py`: Defines `Movie` and `MovieLinks` database structures.
    *   `views.py`: Handles logic for listing, searching, and filtering movies.
    *   `urls.py`: App-specific URL routing.
*   **`templates/`**: HTML templates for the website.
*   **`static/`**: CSS, JavaScript, and static image files.
*   **`media/`**: User-uploaded content (Movie posters and banners).

## Contributing

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature-name`).
3.  Commit your changes (`git commit -m 'Add new feature'`).
4.  Push to the branch (`git push origin feature-name`).
5.  Open a Pull Request.