from django.shortcuts import render, redirect
from . models import Movie, MovieLinks, Comment
from .recommendations import get_recommendations
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import requests

# Create your views here.

def tv_shows(request):
    try:
        response = requests.get('https://api.tvmaze.com/shows')
        response.raise_for_status()
        # Get the first 24 shows to display
        shows = response.json()[:24]
    except requests.RequestException:
        shows = []
    
    return render(request, "movie/tv_shows.html", {"shows": shows})

def profile_view(request):
    if request.method == 'POST':
        profile = request.user.profile
        if request.FILES.get('image'):
            profile.image = request.FILES['image']
            profile.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('movie:profile')
    return render(request, "movie/profile.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Here you would typically send an email
        messages.success(request, f"Thanks {name}! We have received your message.")
        return redirect('movie:contact')
    return render(request, "movie/contact.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("movie:movie")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm()
    return render(request, "movie/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("movie:movie")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "movie/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("movie:movie")

def movies(request):
    movies = Movie.objects.all()
    search_result = request.GET.get("q")
    if search_result:
        movies = movies.filter(
            Q(title__icontains=search_result) |
            Q(description__icontains=search_result) |
            Q(cast__icontains=search_result)
        )
    paginator = Paginator(movies, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "movie/movie_list.html", context={
        "page_obj": page_obj
    })


def movie_details(request, _id: int):
    movie = Movie.objects.get(pk=_id)
    
    # Session-based view counting
    session_key = f'viewed_movie_{_id}'
    if not request.session.get(session_key, False):
        movie.views_count += 1
        movie.save()
        request.session[session_key] = True

    links = MovieLinks.objects.filter(movie_id = _id)
    
    # Use Content-Based Recommendation
    related_movies = get_recommendations(_id)
    
    # Favorites check
    is_favorited = False
    if request.user.is_authenticated:
        if request.user.profile.favorites.filter(pk=_id).exists():
            is_favorited = True

    # Comment Handling
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect("movie:login")
        
        text = request.POST.get("text")
        if text:
            Comment.objects.create(user=request.user, movie=movie, text=text)
            messages.success(request, "Comment added!")
            return redirect("movie:movie_details", _id=_id)

    comments = movie.comments.all().order_by("-created_at")

    return render(request, "movie/movie_details.html", context={
        "movie": movie, 
        "links": links,
        "related_movies": related_movies,
        "is_favorited": is_favorited,
        "comments": comments
    })

def toggle_favorite(request, _id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to manage favorites.")
        return redirect("movie:login")
    
    movie = Movie.objects.get(pk=_id)
    profile = request.user.profile
    
    if profile.favorites.filter(pk=_id).exists():
        profile.favorites.remove(movie)
        messages.info(request, "Removed from favorites.")
    else:
        profile.favorites.add(movie)
        messages.success(request, "Added to favorites.")
        
    return redirect("movie:movie_details", _id=_id)


def filter_by_category(request, category):
    movies = Movie.objects.filter(category=category)
    paginator = Paginator(movies, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "movie/movie_list.html", context={
        "page_obj": page_obj
    })


def filter_by_language(request, language):
    movies = Movie.objects.filter(language=language)
    paginator = Paginator(movies, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "movie/movie_list.html", context={
        "page_obj": page_obj
    })