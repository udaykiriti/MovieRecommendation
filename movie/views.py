from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, MovieLinks, Comment
from .recommendations import get_recommendations
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests

def movies(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query)
        )
    else:
        movies = Movie.objects.all().order_by('-created')

    paginator = Paginator(movies, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    slider_movies = Movie.objects.all().order_by('-created')[:5]
    
    return render(request, "movie/movie_list.html", {'page_obj': page_obj, 'slider_movies': slider_movies})

def movie_details(request, _id):
    movie = get_object_or_404(Movie, pk=_id)
    movie.views_count += 1
    movie.save()
    
    links = MovieLinks.objects.filter(movie=movie)
    related_movies = get_recommendations(_id)
    
    # Comments handling
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, movie=movie, text=text)
            messages.success(request, "Comment posted!")
            return redirect('movie:movie_details', _id=_id)

    comments = movie.comments.all().order_by('-created_at')
    
    is_favorited = False
    is_watchlisted = False
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            if request.user.profile.favorites.filter(pk=_id).exists():
                is_favorited = True
            if request.user.profile.watchlist.filter(pk=_id).exists():
                is_watchlisted = True

    context = {
        'movie': movie,
        'links': links,
        'related_movies': related_movies,
        'comments': comments,
        'is_favorited': is_favorited,
        'is_watchlisted': is_watchlisted,
    }
    return render(request, "movie/movie_details.html", context)

def tv_shows(request):
    try:
        response = requests.get('http://api.tvmaze.com/shows')
        response.raise_for_status()
        shows = response.json()
        # Sort by rating or popularity if possible, or just slice
        # API returns list.
        shows = shows[:50] # Limit to 50
    except requests.RequestException:
        shows = []
    
    return render(request, "movie/tv_shows.html", {'shows': shows})

@login_required
def profile_view(request):
    if not hasattr(request.user, 'profile'):
         from .models import Profile
         Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user = request.user
        profile = user.profile

        # Update User fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        # Update Profile fields
        profile.bio = request.POST.get('bio', profile.bio)
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        profile.save()
        
        messages.success(request, "Profile updated successfully.")
        return redirect('movie:profile')

    return render(request, "movie/profile.html")

def public_profile(request, username):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    return render(request, "movie/public_profile.html", {'profile_user': user})

def toggle_watchlist(request, _id):
    if not request.user.is_authenticated:
        from django.http import HttpResponse
        return HttpResponse('<span style="font-size: 12px; color: red;">Login required</span>', status=200)
    
    movie = get_object_or_404(Movie, pk=_id)
    
    if not hasattr(request.user, 'profile'):
         from .models import Profile
         Profile.objects.create(user=request.user)

    profile = request.user.profile
    
    if profile.watchlist.filter(pk=_id).exists():
        profile.watchlist.remove(movie)
        is_watchlisted = False
    else:
        profile.watchlist.add(movie)
        is_watchlisted = True
        
    return render(request, "partials/watchlist_icon.html", {"is_watchlisted": is_watchlisted})


def contact(request):
    return render(request, "movie/contact.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('movie:movie')
    else:
        form = UserCreationForm()
    return render(request, 'movie/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        # Custom handling since template uses manual inputs
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {u}!")
            return redirect('movie:movie')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'movie/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('movie:movie')

def toggle_favorite(request, _id):
    if not request.user.is_authenticated:
        # If not logged in, we can't toggle.
        # HTMX handles redirects poorly without specific headers, 
        # so we might return a snippet saying "Login" or just 401.
        # For simplicity, let's just return a generic error or redirect URL.
        from django.http import HttpResponse
        return HttpResponse('<span style="font-size: 12px; color: red;">Login required</span>', status=200)
    
    movie = get_object_or_404(Movie, pk=_id)
    
    if not hasattr(request.user, 'profile'):
         from .models import Profile
         Profile.objects.create(user=request.user)

    profile = request.user.profile
    
    if profile.favorites.filter(pk=_id).exists():
        profile.favorites.remove(movie)
        is_favorited = False
    else:
        profile.favorites.add(movie)
        is_favorited = True
        
    return render(request, "partials/favorite_icon.html", {"is_favorited": is_favorited})


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

def search_results(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Movie.objects.filter(title__icontains=query)[:5]
    
    return render(request, 'partials/search_results.html', {'results': results, 'query': query})

def random_movie_data(request):
    """Returns random movie posters and one final winner for the slot machine."""
    import random
    all_movies = list(Movie.objects.all())
    if len(all_movies) < 5:
        return JsonResponse({"error": "Not enough movies"}, status=400)
    
    # Selection for the reel (15 posters)
    reel_movies = random.sample(all_movies, min(len(all_movies), 15))
    winner = random.choice(all_movies)
    
    data = {
        "reel": [{"image": m.image.url} for m in reel_movies],
        "winner": {
            "title": winner.title,
            "url": f"/{winner.id}/",
            "image": winner.image.url
        }
    }
    return JsonResponse(data)

