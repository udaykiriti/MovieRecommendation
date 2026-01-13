import requests
from django.conf import settings
from django.core.files.base import ContentFile
import os

def fetch_tmdb_movie_details(tmdb_id):
    """
    Fetches movie details from TMDb API given a tmdb_id.
    """
    api_key = getattr(settings, 'TMDB_API_KEY', None)
    if not api_key or api_key == 'YOUR_TMDB_API_KEY_HERE':
        return None

    base_url = "https://api.themoviedb.org/3/movie/"
    params = {
        'api_key': api_key,
        'append_to_response': 'credits,videos'
    }

    try:
        response = requests.get(f"{base_url}{tmdb_id}", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract details
        details = {
            'tmdb_id': data.get('id'),
            'title': data.get('title'),
            'description': data.get('overview'),
            'year_of_production': data.get('release_date'),
            'rating': data.get('vote_average'),
            'image_url': f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else None,
            'banner_url': f"https://image.tmdb.org/t/p/original{data.get('backdrop_path')}" if data.get('backdrop_path') else None,
            'cast': ", ".join([c['name'] for c in data.get('credits', {}).get('cast', [])[:5]]),
            'trailer_url': ""
        }

        # Find YouTube trailer
        videos = data.get('videos', {}).get('results', [])
        for video in videos:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                details['trailer_url'] = f"https://www.youtube.com/embed/{video['key']}"
                break
        
        return details
    except requests.RequestException as e:
        print(f"Error fetching TMDb data: {e}")
        return None

def download_image(url):
    """
    Downloads an image from a URL and returns a ContentFile.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return ContentFile(response.content, name=os.path.basename(url))
    except requests.RequestException:
        return None

def search_tmdb_movies(query):
    """
    Searches for movies on TMDb by title.
    """
    api_key = getattr(settings, 'TMDB_API_KEY', None)
    if not api_key or api_key == 'YOUR_TMDB_API_KEY_HERE':
        return []

    url = "https://api.themoviedb.org/3/search/movie"
    params = {'api_key': api_key, 'query': query}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException:
        return []
