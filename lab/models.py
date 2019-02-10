from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import cirpy


class Material(models.Model):
    name = models.CharField(max_length=200)
    specifications = models.CharField(max_length=500, blank=True)
    cas = models.CharField(max_length=50, blank=True, verbose_name='CAS')
    amount = models.IntegerField(default=1, validators=[MaxValueValidator(1000), MinValueValidator(1)])
    location = models.CharField(max_length=500, blank=True)
    msds_url = models.URLField(blank=True, verbose_name='MSDS URL')
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('manage_inventory', 'Can manage inventory'),
        )

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('inventory')

    def save(self, *args, **kwargs):
        # Add CAS number to database if it is a newly created object, so set CAS number
        if not self.cas:
            try:
                query = cirpy.resolve(self.name, 'cas')
                cas_result = query[0]
                for number in query:
                    if len(number) < len(cas_result):
                        cas_result = number
            
                self.cas = cas_result
            except:
                pass

        super(Material, self).save(*args, **kwargs)


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('announcements')
