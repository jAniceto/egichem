from django.urls import path
from . import views


urlpatterns = [
    # path('', views.calculators, name='calculators'),
    path('carbon-dioxide/', views.carbon_dioxide, name='carbon_dioxide'),
    path('isotherms/', views.isotherms, name='isotherms'),
]
