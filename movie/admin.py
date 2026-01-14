from django.contrib import admin
from .models import Movie, MovieLinks, Category, Profile, Comment, Actor
from .tmdb_utils import fetch_tmdb_movie_details, download_image, search_tmdb_movies
from django.contrib import messages

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'language', 'status', 'year_of_production', 'tmdb_id', 'rating']
    search_fields = ['title', 'description', 'cast__name', 'category__name']
    list_filter = ['category', 'language', 'status']
    actions = ['sync_with_tmdb']
    
    def sync_with_tmdb(self, request, queryset):
        count = 0
        for movie in queryset:
            if movie.tmdb_id:
                details = fetch_tmdb_movie_details(movie.tmdb_id)
                if details:
                    movie.title = details['title']
                    movie.description = details['description']
                    movie.year_of_production = details['year_of_production']
                    movie.rating = details['rating']
                    movie.movie_trailer = details['trailer_url']
                    movie.save()
                    
                    if details['cast']:
                        actor_objs = []
                        for actor_name in details['cast']:
                            actor, _ = Actor.objects.get_or_create(name=actor_name)
                            actor_objs.append(actor)
                        movie.cast.set(actor_objs)
                    
                    count += 1
        self.message_user(request, f"Successfully synced {count} movies with TMDb.")
    sync_with_tmdb.short_description = "Sync selected movies with TMDb"
    
    def save_model(self, request, obj, form, change):
        # If tmdb_id is provided and we are either creating or title/desc are missing
        if obj.tmdb_id and (not obj.title or not obj.description):
            details = fetch_tmdb_movie_details(obj.tmdb_id)
            if details:
                obj.title = details['title']
                obj.description = details['description']
                obj.year_of_production = details['year_of_production']
                obj.rating = details['rating']
                obj.movie_trailer = details['trailer_url']
                
                # Fetch images if not already present
                if not obj.image and details['image_url']:
                    img_file = download_image(details['image_url'])
                    if img_file:
                        obj.image.save(f"{obj.tmdb_id}_poster.jpg", img_file, save=False)
                
                if not obj.banner and details['banner_url']:
                    banner_file = download_image(details['banner_url'])
                    if banner_file:
                        obj.banner.save(f"{obj.tmdb_id}_banner.jpg", banner_file, save=False)
                
                obj.save() # Save object first to allow M2M assignment
                
                if details['cast']:
                    actor_objs = []
                    for actor_name in details['cast']:
                        actor, _ = Actor.objects.get_or_create(name=actor_name)
                        actor_objs.append(actor)
                    obj.cast.set(actor_objs)

                messages.success(request, f"Successfully imported details for '{obj.title}' from TMDb.")
            else:
                messages.error(request, f"Could not fetch details for TMDb ID {obj.tmdb_id}. Please check your API key.")
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor)
admin.site.register(MovieLinks)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)