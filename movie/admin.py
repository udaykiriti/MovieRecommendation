from django.contrib import admin
from .models import Movie, MovieLinks, Category, Profile, Comment
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'language', 'status', 'year_of_production', 'views_count']
    search_fields = ['title', 'description', 'cast']
    list_filter = ['category', 'language', 'status']

admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieLinks)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)