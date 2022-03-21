from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from website.models import Member
from datetime import datetime
import cirpy


class Material(models.Model):
    TYPES = (
        ('Reagent', 'Reagent'),
        ('Material', 'Material'),
        ('Tool', 'Tool'),
        ('Other', 'Other'),
    )
    item_type = models.CharField(max_length=50, choices=TYPES, default='Reagent')
    name = models.CharField(max_length=200)
    specifications = models.CharField(max_length=500, blank=True)
    cas = models.CharField(max_length=50, blank=True, verbose_name='CAS')
    amount = models.IntegerField(default=1, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    location = models.CharField(max_length=500, blank=True)
    msds_url = models.URLField(blank=True, verbose_name='MSDS URL')
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,)

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

    class Meta:
        permissions = (
            ('manage_inventory', 'Can manage inventory'),
        )

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('announcements')


class ExternalResource(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    resource_type = models.TextField(blank=True)
    url1 = models.URLField()
    url1_text = models.CharField(max_length=15, default='Link')
    url2 = models.URLField(blank=True)
    url2_text = models.CharField(max_length=15, default='Link2')
    url3 = models.URLField(blank=True)
    url3_text = models.CharField(max_length=15, default='Link3')
    date_added = models.DateTimeField(default=timezone.now)
    order = models.IntegerField(default=99)

    # class Meta:
    #     permissions = (
    #         ('manage_inventory', 'Can manage inventory'),
    #     )

    def __str__(self):
        return f'{self.title}'


class LabTeam(models.Model):
    class Month(models.IntegerChoices):
        JANUARY = 1
        FEBRUARY = 2
        MARCH = 3
        APRIL = 4
        MAY = 5
        JUNE = 6
        JULY = 7
        AUGUST = 8
        SEPTEMBER = 9
        OCTOBER = 10
        NOVEMBER = 11
        DECEMBER = 12

    month = models.IntegerField(choices=Month.choices, default=datetime.now().month)
    year = models.IntegerField(default=datetime.now().year)
    cleaning = models.ManyToManyField(Member, related_name='cleaning_team', limit_choices_to={'alumni': False}, blank=True)
    technic = models.ManyToManyField(Member, related_name='technic_team', limit_choices_to={'alumni': False}, blank=True)
    safety = models.ManyToManyField(Member, related_name='safety_team', limit_choices_to={'alumni': False}, blank=True)
    # created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.year}/{self.month} Teams'