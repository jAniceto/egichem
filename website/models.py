from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User


class ResearchField(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images', default='/Users/USER/Dropbox/Projectos/egichem/media/images/350x200.png')
    date_posted = models.DateTimeField(default=timezone.now)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title