from movie.models import Movie, Actor

movies = Movie.objects.all()
for movie in movies:
    if movie.cast:
        actor_names = [name.strip() for name in movie.cast.split(',') if name.strip()]
        for name in actor_names:
            actor, created = Actor.objects.get_or_create(name=name)
            movie.new_cast.add(actor)
        print(f"Processed {movie.title}: {len(actor_names)} actors")