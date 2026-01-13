import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.core.cache import cache
from .models import Movie

CACHE_TIMEOUT = 24 * 60 * 60  # 24 hours

def get_recommendations(movie_id, total_results=6):
    """
    Returns a list of Movie objects similar to the given movie_id.
    First checks the cache. If not found, computes on the fly (expensive).
    """
    cache_key = f"rec_movie_{movie_id}"
    cached_ids = cache.get(cache_key)

    if cached_ids is not None:
        # Fetch movies from DB to ensure they still exist and return actual objects
        # We need to preserve order, so we can't just use filter(id__in=...) directly
        recommended_movies = []
        movies_dict = {m.id: m for m in Movie.objects.filter(id__in=cached_ids)}
        
        for rid in cached_ids:
            if rid in movies_dict:
                recommended_movies.append(movies_dict[rid])
        return recommended_movies

    # Fallback: Compute just for this movie (or trigger full update?)
    # For now, we use the existing logic to compute on the fly if cache misses.
    return _compute_single_recommendation(movie_id, total_results)


def compute_all_recommendations():
    """
    Computes the similarity matrix for ALL movies at once and caches
    the results for every single movie.
    To be called by a background task or management command.
    """
    movies = list(Movie.objects.all())
    if len(movies) < 3:
        return

    # 1. Build DataFrame
    data = []
    for m in movies:
        cat_name = ""
        if hasattr(m, 'category') and m.category:
            if hasattr(m.category, 'name'): 
                cat_name = m.category.name
            else: 
                cat_name = str(m.category)
        
        data.append({
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'cast': m.cast,
            'category': cat_name
        })
    
    df = pd.DataFrame(data)

    def combine_features(row):
        return f"{row['title']} {row['category']} {row['cast']} {row['description']}"

    df['combined_features'] = df.apply(combine_features, axis=1)

    # 2. Vectorize & Compute Similarity
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 3. Iterate over every movie and cache its recommendations
    # cosine_sim is a square matrix (N x N)
    indices = pd.Series(df.index, index=df['id']).drop_duplicates()

    for movie in movies:
        try:
            idx = indices[movie.id]
            
            # Get similarity scores for this movie
            sim_scores = list(enumerate(cosine_sim[idx]))
            
            # Sort
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Top 6 (excluding self at index 0)
            sim_scores = sim_scores[1:7]
            
            # Get indices
            movie_indices = [i[0] for i in sim_scores]
            
            # Map back to DB IDs
            rec_ids = df['id'].iloc[movie_indices].tolist()
            
            # Set cache
            cache.set(f"rec_movie_{movie.id}", rec_ids, CACHE_TIMEOUT)
            
        except KeyError:
            continue
            
    print(f"Successfully cached recommendations for {len(movies)} movies.")


def _compute_single_recommendation(movie_id, total_results=6):
    """
    The original logic, extracted to run only when cache misses.
    """
    movies = Movie.objects.all()
    if movies.count() < 3:
        return list(Movie.objects.exclude(id=movie_id)[:total_results])

    data = []
    for m in movies:
        cat_name = ""
        if hasattr(m, 'category') and m.category:
            if hasattr(m.category, 'name'):
                cat_name = m.category.name
            else:
                cat_name = str(m.category)
        
        data.append({
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'cast': m.cast,
            'category': cat_name
        })
    
    df = pd.DataFrame(data)

    def combine_features(row):
        return f"{row['title']} {row['category']} {row['cast']} {row['description']}"

    df['combined_features'] = df.apply(combine_features, axis=1)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    try:
        indices = pd.Series(df.index, index=df['id']).drop_duplicates()
        idx = indices[movie_id]
    except KeyError:
        return []

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:total_results+1]
    movie_indices = [i[0] for i in sim_scores]

    recommended_ids = df['id'].iloc[movie_indices].tolist()
    
    # Cache this result since we did the work anyway
    cache.set(f"rec_movie_{movie_id}", recommended_ids, CACHE_TIMEOUT)

    recommended_movies = list(Movie.objects.filter(id__in=recommended_ids))
    recommended_movies.sort(key=lambda x: recommended_ids.index(x.id))
    
    return recommended_movies