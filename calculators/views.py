from django.shortcuts import render
from .forms import CarbonDioxideForm, IsothermForm

from properties import CO2, CO2_EtOH, EtOH
import numpy as np


def carbon_dioxide(request):

    if request.method == 'POST':
        form = CarbonDioxideForm(request.POST)
        # print('valid', form.is_valid())

        if form.is_valid():
            cosolvent = form.cleaned_data['cosolvent']
            temperature = form.cleaned_data['temperature']
            pressure = form.cleaned_data['pressure']
            cosolvent_fraction = form.cleaned_data['cosolvent_fraction']

            if cosolvent == 'NONE':
                # Calculate pure CO2 density and viscosity
                CO2_dens = CO2.get_density(pressure, temperature)
                CO2_visc = CO2.get_viscosity(temperature, CO2_dens)
                density = f'{CO2_dens:.8f}'
                viscosity = f'{CO2_visc:.8f}'
            
            elif cosolvent == 'ETHANOL':
                # Calculate pure CO2-EtOH density and viscosity
                CO2EtOH_dens = CO2_EtOH.get_density(pressure, temperature, cosolvent_fraction)
                CO2EtOH_visc = CO2_EtOH.get_viscosity(pressure, temperature, cosolvent_fraction)
                density = f'{CO2EtOH_dens:.8f}'
                viscosity = f'{CO2EtOH_visc:.8f}'

        else:
            density = ''
            viscosity = ''
    
    else:
        form = CarbonDioxideForm()
        density = ''
        viscosity = ''

    context = {
		'page_title': 'Tools',
        'page_subtitle': 'Programs developed by the EgiChem Group',
        'form': form,
        'density': density,
        'viscosity': viscosity
	}	
    return render(request, 'calculators/carbon_dioxide.html', context)


def parse_XY_data(data):
    """Parse XY data"""
    X_data = []
    Y_data = []
    for line in data.splitlines():
        # line = line.strip()
        xy = line.split(' ')
        X_data.append(float(xy[0]))
        Y_data.append(float(xy[1]))
    return np.array(X_data), np.array(Y_data)


def isotherms(request):

    if request.method == 'POST':
        form = IsothermForm(request.POST)

        if form.is_valid():
            xy_data = form.cleaned_data['xy_data']
            x, y = parse_XY_data(xy_data)
            print(x)
            print(y)
    
    else:
        form = IsothermForm()

    context = {
		'page_title': 'Tools',
        'page_subtitle': 'Programs developed by the EgiChem Group',
        'form': form,
	}
    return render(request, 'calculators/isotherms.html', context)