from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


class TestUserViews(TestCase):

    def setUp(self):
        self.client: Client()

        self.user = User.objects.create(username='Test User', email='testuser@test.com', password='testuser123')

        self.profile = Profile()
        self.profile.user = self.user
        self.profile.bio_text = 'Hi, lovely people!'
        self.profile.profile_image = 'profile_images/image_profile.jpg'
        self.profile.save()

    def test_profile_detail(self):
        ''' Test if view loads a page '''
        response = self.client.get(reverse('profile-detail', args=[self.profile]))
        self.assertEqual(response.status_code, 200)
