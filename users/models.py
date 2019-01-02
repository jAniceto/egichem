from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='images/profile_photos/default.jpg', upload_to='images/profile_photos')
    bio = models.TextField(blank=True)
    scholar_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    scopus_url = models.URLField(blank=True)
    cv_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'