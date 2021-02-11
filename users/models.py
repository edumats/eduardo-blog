from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio_text = models.TextField()
    profile_image = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return self.user.username
