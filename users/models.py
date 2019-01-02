from django.db import models
from django.contrib.auth.models import User
from PIL import Image


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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
