from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculators_home, name='calculators_home'),
    path('carbon-dioxide/', views.carbon_dioxide, name='carbon_dioxide'),
    path('isotherms/', views.isotherms, name='isotherms'),
    path('d12-sc-co2/', views.d12_sc_co2, name='d12_sc_co2'),
    path('d12-polar-nonpolar/', views.d12_polar_nonpolar, name='d12_polar_nonpolar'),
    path('psychrometrics/', views.psychrometrics, name='psychrometrics'),
]
