from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='images/profile_photos/default.jpg', upload_to='images/profile_photos')
    scientific_name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    scholar_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    scopus_url = models.URLField(blank=True)
    personal_url = models.URLField(blank=True)
    research_gate_url = models.URLField(blank=True)
    orcid_url = models.URLField(blank=True)
    ciencia_id = models.CharField(max_length=50, blank=True)

    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    
    # Override the save method to handle image upload (reduce size and crop)
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(storage.open(self.photo.name))
        
    #     # Reduce size of image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
            
    #         # Crop image to square
    #         if img.width != img.height:
    #             w, h = img.size
    #             cropped = img.crop((w//2 - 300//2, h//2 - 300//2, w//2 + 300//2, h//2 + 300//2))
    #             cropped.save(storage.open(self.photo.name))

    #         else:
    #             img.save(storage.open(self.photo.name))
