from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='images/profile_photos/default.jpg', upload_to='images/profile_photos')
    scientific_name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    scholar_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    scopus_url = models.URLField(blank=True)
    personal_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)
        
        # Crop image to square
        w, h = img.size  
        if img.height > 300 or img.width > 300:
            if img.width != img.height:
                cropped = img.crop((w//2 - 300//2, h//2 - 300//2, w//2 + 300//2, h//2 + 300//2))
                cropped.save(self.photo.path)

            # Reduce size of image
            else:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)
