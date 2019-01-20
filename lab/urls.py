from django.urls import path
from .views import MaterialListView
from . import views


urlpatterns = [
    # path('', views.home, name='home'),
    # path('inventory/', views.inventory, name='inventory'),
    path('inventory/', MaterialListView.as_view(), name='inventory'),
]
