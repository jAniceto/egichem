from django.shortcuts import render
from .forms import CarbonDioxideForm

from properties import CO2, CO2_EtOH


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
                print('CO2 density:', CO2_dens)
                CO2_visc = CO2.get_viscosity(temperature, CO2_dens)
                print('CO2 viscosity in cP:', CO2_visc)
                density = f'{CO2_dens:.8f}'
                viscosity = f'{CO2_visc:.8f}'
            
            elif cosolvent == 'ETHANOL':
                # Calculate pure CO2-EtOH density
                CO2EtOH_dens = CO2_EtOH.get_density(pressure, temperature, cosolvent_fraction)
                print('CO2-EtOH density:', CO2EtOH_dens)
                density = f'{CO2EtOH_dens:.8f}'
                viscosity = ''

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