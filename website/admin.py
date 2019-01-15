from django.contrib import admin
from .models import ResearchField, LabUnit, Partner, Collaborator, Member, Publication, Award


admin.site.register(ResearchField)
admin.site.register(LabUnit)
admin.site.register(Partner)
admin.site.register(Collaborator)
admin.site.register(Member)
admin.site.register(Publication)
admin.site.register(Award)
