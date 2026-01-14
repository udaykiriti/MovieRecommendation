from movie.models import Movie, Category

def migrate_categories():
    movies = Movie.objects.all()
    for movie in movies:
        if movie.category:
            # The category field currently holds lowercase keys like 'action', 'drama'
            cat_name = movie.category.title() # Convert 'action' -> 'Action'
            
            # Get or create the Category object
            category_obj, created = Category.objects.get_or_create(name=cat_name)
            
            # Add to M2M field
            movie.genres.add(category_obj)
            print(f"Mapped '{movie.title}' to Category: {cat_name}")

migrate_categories()
