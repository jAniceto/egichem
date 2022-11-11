from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculators_home, name='calculators_home'),
    path('carbon-dioxide/', views.carbon_dioxide, name='carbon_dioxide'),
    path('isotherms/', views.isotherms, name='isotherms'),
    path('d12-sc-co2/', views.d12_sc_co2, name='d12_sc_co2'),
    path('d12-sc-co2-old/', views.d12_sc_co2_old, name='d12_sc_co2_old'),  # to delete in future
    path('d12-polar-nonpolar/', views.d12_polar_nonpolar, name='d12_polar_nonpolar'),
    path('d12-polar-nonpolar-old/', views.d12_polar_nonpolar_old, name='d12_polar_nonpolar_old'),  # to delete in future
    path('psychrometrics/', views.psychrometrics, name='psychrometrics'),
    path('psychrometrics-vent/', views.psychrometrics_ventilation, name='psychrometrics_ventilation'),
    path('unit-conversion/', views.unit_conversion, name='unit_conversion'),
    path('air-properties/', views.air_properties, name='air_properties'),
    path('pcsaft-co2/', views.pcsaft_co2, name='pcsaft_co2'),
    path('pcsaft/', views.pcsaft, name='pcsaft'),
    path('utilities/', views.utilities, name='utilities'),
    path('d12-gas/', views.d12_gas, name='d12_gas'),
    path('d12-rg/', views.d12_rg, name='d12_rg'),
    path('klinkenberg/', views.klinkenberg, name='klinkenberg'),
    path('joback/', views.joback, name='joback'),
]
