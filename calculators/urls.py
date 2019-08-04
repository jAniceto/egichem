from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculators_home, name='calculators_home'),
    path('carbon-dioxide/', views.carbon_dioxide, name='carbon_dioxide'),
    path('isotherms/', views.isotherms, name='isotherms'),
]
