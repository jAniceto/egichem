from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialDeleteView, MaterialUpdateView, AnnouncementListView, AnnouncementCreateView
from . import views


urlpatterns = [
    path('', views.egichem, name='egichem'),
    # path('inventory/', views.inventory, name='inventory'),
    path('inventory/', MaterialListView.as_view(), name='inventory'),
    path('inventory/material/new/', MaterialCreateView.as_view(), name='material-create'),
    path('inventory/material/<int:pk>/update/', MaterialUpdateView.as_view(), name='material-update'),
    path('inventory/material/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material-delete'),
    path('inventory/export/', views.export, name='export'),
    path('announcements/', AnnouncementListView.as_view(), name='announcements'),
    path('announcements/new/', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement-delete'),
    path('lab-teams/', views.lab_teams, name='lab_teams'),
]
