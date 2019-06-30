from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify


class ResearchField(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(default='images/350x200.png', upload_to='images/research-fields')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class LabUnit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    equipment = models.TextField()
    image = models.ImageField(default='images/placeholder.png', upload_to='images/lab')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Collaborator(models.Model):
    name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=200)
    scope = models.CharField(max_length=500)
    link = models.URLField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=100)
    scope = models.CharField(max_length=500, blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(default='images/350x200.png', upload_to='images/partners')
    date_added = models.DateTimeField(default=timezone.now)

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
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='member')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITIONS)
    research_area = models.CharField(max_length=200, blank=True)
    thesis = models.TextField(blank=True)
    photo = models.ImageField(default='images/profile_photos/default.jpg', upload_to='images/people', blank=True)
    alumni = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Member, self).save(*args, **kwargs)


class Publication(models.Model):
    PUB_TYPES = (
        ('article', 'Articles'),
        ('book-chapter', 'Book Chapter'),
        ('patent', 'Patent'),
        ('poster', 'Poster'),
        ('presentation', 'Presentation'),
        ('thesis', 'Thesis'),
    )
    THESIS_TYPES = (
        ('MSc', 'MSc Thesis'),
        ('PhD', 'PhD Thesis'),
    )
    pub_type = models.CharField(max_length=50, choices=PUB_TYPES)
    authors = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    year = models.CharField(max_length=10)
    journal = models.CharField(max_length=500, blank=True)
    volume = models.CharField(max_length=10, blank=True)
    issue = models.CharField(max_length=10, blank=True)
    pages = models.CharField(max_length=20, blank=True)
    link = models.URLField(blank=True)
    book_title = models.CharField(max_length=500, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    abstract = models.TextField(blank=True)
    patent_number = models.CharField(max_length=100, blank=True)
    conference = models.CharField(max_length=200, blank=True)
    conference_city = models.CharField(max_length=100, blank=True)
    conference_date = models.CharField(max_length=100, blank=True)
    thesis_type = models.CharField(max_length=15, choices=THESIS_TYPES, blank=True)
    thesis_coordinators = models.CharField(max_length=500, blank=True)
    thesis_institution = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(default='images/publications/book_placeholder.jpg', upload_to='images/publications')

    def __str__(self):
        return f'{self.pub_type} - {self.title}'


class Tool(models.Model):
    title = models.CharField(max_length=250)
    filetype = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(default='tools/tools-placeholder.png', upload_to='tools/')
    program_file = models.FileField(upload_to='tools/', blank=True)
    help_file = models.FileField(upload_to='tools/', blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'


class Award(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, blank=True)
    awarded_to = models.CharField(max_length=500, blank=True)
    awarded_for = models.CharField(max_length=500, blank=True)
    link = models.URLField(blank=True)
    image = models.ImageField(default='images/awards/award-placeholder.png', upload_to='images/awards')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}'