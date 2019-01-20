from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialDeleteView, MaterialUpdateView
from . import views


urlpatterns = [
    # path('', views.home, name='home'),
    # path('inventory/', views.inventory, name='inventory'),
    path('inventory/', MaterialListView.as_view(), name='inventory'),
    path('inventory/material/new/', MaterialCreateView.as_view(), name='material-create'),
    path('inventory/material/<int:pk>/update/', MaterialUpdateView.as_view(), name='material-update'),
    path('inventory/material/<int:pk>/delete/', MaterialDeleteView.as_view(), name='material-delete'),
]
