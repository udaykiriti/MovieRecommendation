from django.shortcuts import render
from . models import Movie, MovieLinks
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def movies(request):
    movies = Movie.objects.all()
    search_result = request.GET.get("q")
    if search_result:
        movies = movies.filter(
            Q(title__icontains=search_result)
        )
    paginator = Paginator(movies, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "movie/movie_list.html", context={
        "page_obj": page_obj
    })


def movie_details(request, _id: int):
    movie = Movie.objects.get(pk=_id)
    movie.views_count += 1
    movie.save()
    links = MovieLinks.objects.filter(movie_id = _id)
    related_movies = Movie.objects.filter(category=movie.category).exclude(pk=_id)
    return render(request, "movie/movie_details.html", context={
        "movie": movie, 
        "links": links,
        "related_movies": related_movies
    })


def filter_by_category(request, category):
    movies = Movie.objects.filter(category=category)
    paginator = Paginator(movies, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "movie/movie_list.html", context={
        "page_obj": page_obj
    })


def filter_by_language(request, language):
    movies = Movie.objects.filter(language=language)
    paginator = Paginator(movies, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "movie/movie_list.html", context={
        "page_obj": page_obj
    })