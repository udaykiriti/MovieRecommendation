from tabnanny import verbose
from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


CATEGORY_CHOICES = (
    ('action','ACTION'),
    ('drama','DRAMA'),
    ('comedy','COMEDY'),
    ('romance','ROMANCE'),
)

LANGUAGE_CHOICES = (
    ('english' , 'ENGLISH'),
    ('german' , 'GERMAN'),
)

STATUS_CHOICES = (
    ('RA' , 'RECENTLY ADDED'),
    ('MW' , 'MOST WATCHED'),
    ('TR' , 'TOP RATED'),
)



class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="movies")
    banner = models.ImageField(upload_to='movies_banner')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=2)
    cast = models.CharField(max_length=100)
    year_of_production = models.DateField()
    views_count = models.IntegerField(default=0)
    movie_trailer = models.URLField()
    created = models.DateTimeField(default=datetime.now)
    slug = models.SlugField(blank=True, null=True)
    

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super(Movie , self).save(*args , **kwargs)



    def __str__(self) -> str:
        return self.title



LINK_CHOICES = (
    ('D' , 'DOWNLOAD LINK'),
    ('W' , 'WATCH LINK'),
)


class MovieLinks(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    link_type = models.CharField(choices=LINK_CHOICES, max_length=1)
    link = models.URLField()


    class Meta:
        verbose_name = "Movie Link"
        

    def __str__(self) -> str:
        return self.movie.title

# User Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)
    favorites = models.ManyToManyField(Movie, blank=True, related_name='favorited_by')
    watchlist = models.ManyToManyField(Movie, blank=True, related_name='watchlisted_by')

    def __str__(self):
        return f'{self.user.username} Profile'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'

# Signals to auto-create profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
