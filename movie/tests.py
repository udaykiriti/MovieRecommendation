from django.test import TestCase, Client
from django.urls import reverse
from .models import Movie, Category, Profile
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class MovieViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        # Ensure profile exists (signals might have created it)
        if not hasattr(self.user, 'profile'):
            Profile.objects.create(user=self.user)
            
        self.user_no_profile = User.objects.create_user(username='noprofile', password='password')
        # Manually delete profile if signal created it, to simulate the error condition
        if hasattr(self.user_no_profile, 'profile'):
            self.user_no_profile.profile.delete()
            # Refresh from db to ensure it's gone from cache
            self.user_no_profile.refresh_from_db()

        self.category = Category.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            category='action',
            language='english',
            status='RA',
            cast='Test Cast',
            year_of_production=timezone.now().date(),
            movie_trailer='https://youtube.com',
            image='movies/test.jpg',
            banner='movies_banner/test.jpg'
        )

    def test_movies_view(self):
        response = self.client.get(reverse('movie:movie'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_movie_details_view(self):
        response = self.client.get(reverse('movie:movie_details', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_movie_details_missing_profile(self):
        """Test that a logged-in user with no profile doesn't crash the details view"""
        self.client.login(username='noprofile', password='password')
        response = self.client.get(reverse('movie:movie_details', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        
    def test_toggle_favorite_creates_profile(self):
        """Test that toggle_favorite creates a profile if missing"""
        self.client.login(username='noprofile', password='password')
        response = self.client.get(reverse('movie:toggle_favorite', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.user_no_profile.refresh_from_db()
        self.assertTrue(hasattr(self.user_no_profile, 'profile'))
        self.assertTrue(self.user_no_profile.profile.favorites.filter(id=self.movie.id).exists())

    def test_tv_shows_view(self):
        # This one makes an external request. It handles exceptions so it should be 200 regardless.
        response = self.client.get(reverse('movie:tv_shows'))
        self.assertEqual(response.status_code, 200)
