from django.contrib import admin
from .models import Material, Announcement, ExternalResource


admin.site.register(Material)
admin.site.register(Announcement)
admin.site.register(ExternalResource)