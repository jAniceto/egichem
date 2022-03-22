from django.contrib import admin
from .models import Material, Announcement, ExternalResource, LabTeam, Faq


admin.site.register(Material)
admin.site.register(Announcement)
admin.site.register(ExternalResource)
admin.site.register(LabTeam)
admin.site.register(Faq)
