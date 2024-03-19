from . models import Movie

def slider_movie(request):
    movie = Movie.objects.last()

    return {"movie": movie}