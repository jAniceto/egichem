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


class LabUnit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    equipment = models.TextField()
    image = models.ImageField(upload_to='images/lab')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Collaborator(models.Model):
    name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=200)
    scope = models.CharField(max_length=500)
    link = models.URLField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=100)
    scope = models.CharField(max_length=500, blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(upload_to='images/partners')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Member(models.Model):
    POSITIONS = (
        ('Professor', 'Professor'),
        ('PostDoc Researcher', 'PostDoc Researcher'),
        ('PhD Student', 'PhD Student'),
        ('Research Fellow', 'Research Fellow'),
        ('MSc Student', 'MSc Student'),
        ('Undergraduate Student', 'Undergraduate Student'),
    )
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITIONS)
    research_area = models.CharField(max_length=200, blank=True)
    thesis = models.TextField(blank=True)
    photo = models.ImageField(upload_to='images/people', blank=True)
    alumni = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    # user = models.OneToOneField()

    def __str__(self):
        return self.name