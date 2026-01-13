from . models import Movie, Category

def slider_movie(request):
    movie = Movie.objects.last()
    return {"movie": movie}

def categories_processor(request):
    categories = Category.objects.all()
    return {"categories_list": categories}