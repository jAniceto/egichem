from django.contrib import admin
from .models import Material, Announcement, ExternalResource, LabTeam


admin.site.register(Material)
admin.site.register(Announcement)
admin.site.register(ExternalResource)
admin.site.register(LabTeam)


# class LabTeamAdmin(admin.ModelAdmin):
#     def get_form(self, request, obj=None, **kwargs):
#         form = super(LabTeamAdmin, self).get_form(request, obj, **kwargs)
#         form.base_fields['cleaning'].queryset = LabTeam.objects.filter(Alumni=False)
#         return form
