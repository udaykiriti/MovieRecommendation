# GrandLine Cinema - The Pirate Movie Hub 

A modern, feature-rich movie recommendation platform built with Django. **GrandLine Cinema** offers a sleek, "Netflix-style" browsing experience, complete with an immersive hero slider, real-time interactions, and personalized user profiles.

## Key Features

### Immersive UI/UX
*   **Cinematic Hero Slider:** A responsive, full-screen featured movie slider with video trailers and a smooth vignette effect.
*   **Glassmorphism Design:** Modern, translucent UI elements for a premium feel.
*   **Responsive Layout:** Fully optimized for desktop, tablet, and mobile devices.

### Discovery & Interaction
*   **Smart Search:** Real-time search with **Voice Command** support ("Search for...") powered by HTMX and Web Speech API.
*   **"Surprise Me" Machine:** A fun, slot-machine style random movie picker.
*   **Advanced Filtering:** Browse by Genre (Action, Drama, etc.) and Language.
*   **TV Shows:** Browse popular TV shows fetched from external APIs.

###  User Personalization
*   **User Profiles:** customizable profiles with avatars and bio.
*   **Watchlist & Favorites:** Add movies to your personal collections with one click.
*   **Comments System:** Engage with the community by leaving comments on movies.

## Tech Stack

*   **Backend:** Python 3, Django 4.x
*   **Frontend:** HTML5, CSS3 (Modular), JavaScript (ES6+)
*   **Libraries:**
    *   **HTMX:** For seamless, SPA-like interactions without full page reloads.
    *   **Swiper.js:** For the touch-enabled, responsive sliders.
    *   **jQuery:** For DOM manipulation and effects.
*   **Database:** SQLite (Default) / PostgreSQL ready

##  Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd MovieRecommendation
```

### 2. Set Up Virtual Environment
It's recommended to use a virtual environment.

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
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Apply migrations to create the database schema.
```bash
python manage.py migrate
```

### 5. Create Admin User
To manage movies and users:
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

*   **`movie/`**: Core application logic.
    *   `models.py`: Database schemas (Movie, Profile, Comment, etc.).
    *   `views.py`: Business logic and request handling.
*   **`templates/`**:
    *   `auth/`: Login/Signup pages.
    *   `movies/`: Lists and Detail views.
    *   `pages/`: Profile, Contact, and static pages.
    *   `partials/`: Reusable HTMX components (icons, search results).
*   **`static/`**:
    *   `css/`: Modular stylesheets (`base.css`, `pages/home.css`, etc.).
    *   `js/`: Custom scripts and libraries.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---
