from django.contrib import admin
from .models import ResearchField, LabUnit, Partner, Collaborator


admin.site.register(ResearchField)
admin.site.register(LabUnit)
admin.site.register(Partner)
admin.site.register(Collaborator)