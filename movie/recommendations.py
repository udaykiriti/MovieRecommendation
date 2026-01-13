import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Movie

def get_recommendations(movie_id, total_results=6):
    """
    Returns a list of Movie objects similar to the given movie_id
    based on Content-Based Filtering (Title, Description, Category, Cast).
    """
    
    # 1. Fetch all movies from the database
    movies = Movie.objects.all()
    
    # If we don't have enough data, just return generic recommendations
    if movies.count() < 3:
        return Movie.objects.exclude(id=movie_id)[:total_results]

    # 2. Convert QuerySet to DataFrame for easier manipulation
    # We include fields that define the "content" of the movie
    data = []
    for m in movies:
        # Determine category name (handle both ForeignKey and legacy string)
        cat_name = ""
        if hasattr(m, 'category') and m.category:
            if hasattr(m.category, 'name'): # It's a ForeignKey to Category model
                cat_name = m.category.name
            else: # It's a string (legacy)
                cat_name = str(m.category)
        
        data.append({
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'cast': m.cast,
            'category': cat_name
        })
    
    df = pd.DataFrame(data)

    # 3. Create a "soup" of data - combining all text features into one string
    # We give more weight to Category and Cast by repeating them, if desired, 
    # but for now a simple concatenation is a good start.
    def combine_features(row):
        return f"{row['title']} {row['category']} {row['cast']} {row['description']}"

    df['combined_features'] = df.apply(combine_features, axis=1)

    # 4. TF-IDF Vectorization
    # stop_words='english' removes common words like "the", "a", "is"
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    # 5. Compute Cosine Similarity
    # linear_kernel is equivalent to cosine_similarity for normalized vectors but faster
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 6. Get the index of the movie that matches the movie_id
    try:
        indices = pd.Series(df.index, index=df['id']).drop_duplicates()
        idx = indices[movie_id]
    except KeyError:
        # Fallback if ID not found in dataframe (shouldn't happen)
        return Movie.objects.none()

    # 7. Get the similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 8. Sort the movies based on the similarity scores (descending)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 9. Get the scores of the top similar movies (excluding itself at index 0)
    sim_scores = sim_scores[1:total_results+1]

    # 10. Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # 11. Return the actual Movie objects
    # We fetch by IDs to preserve the order of recommendation
    recommended_ids = df['id'].iloc[movie_indices].tolist()
    
    # Django's "in" filter doesn't preserve order, so we sort manually
    recommended_movies = list(Movie.objects.filter(id__in=recommended_ids))
    recommended_movies.sort(key=lambda x: recommended_ids.index(x.id))
    
    return recommended_movies
