from django.contrib import admin
from .models import MainResearchArea, ResearchField, LabUnit, Partner, Collaborator, Member, Publication, Tool, Award


admin.site.register(MainResearchArea)
admin.site.register(ResearchField)
admin.site.register(LabUnit)
admin.site.register(Partner)
admin.site.register(Collaborator)
admin.site.register(Member)
admin.site.register(Publication)
admin.site.register(Tool)
admin.site.register(Award)
