from django.shortcuts import render
from django.http import JsonResponse
from .forms import CarbonDioxideForm, IsothermForm

from properties import CO2, CO2_EtOH, EtOH
from properties import isotherms as isoT
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
            isotherm_types = form.cleaned_data['isotherm_type']
            x, y = parse_XY_data(xy_data)

            data_in = {
                'x': x.tolist(),
                'y': y.tolist(),
                'isotherm_types': isotherm_types,
            }
            data_out = dict()
            if 'linear' in isotherm_types:
                linear = isoT.Linear()
                linear.fit(x, y)
                ycalc_linear = linear.isotherm(x)
                aard_linear = linear.aard(ycalc_linear)*100
                data_out['Linear'] = {
                    'ycalc': ycalc_linear.tolist(),
                    'params': {k: v for k, v in zip(linear.parameter_names, linear.parameters)},
                    'aard': aard_linear,
                    'xmodel': linear.xmodel.tolist(),
                    'ymodel': linear.ymodel.tolist()
                }

            if 'langmuir' in isotherm_types:
                langmuir = isoT.Langmuir()
                langmuir.fit(x, y)
                ycalc_langmuir = langmuir.isotherm(x)
                aard_langmuir = langmuir.aard(ycalc_langmuir)*100
                data_out['Langmuir'] = {
                    'ycalc': ycalc_langmuir.tolist(),
                    'params': {k: v for k, v in zip(langmuir.parameter_names, langmuir.parameters)},
                    'aard': aard_langmuir,
                    'xmodel': langmuir.xmodel.tolist(),
                    'ymodel': langmuir.ymodel.tolist()
                }

            if 'linearlangmuir' in isotherm_types:
                linearlangmuir = isoT.LinearLangmuir()
                linearlangmuir.fit(x, y)
                ycalc_linearlangmuir = linearlangmuir.isotherm(x)
                aard_linearlangmuir = linearlangmuir.aard(ycalc_linearlangmuir)*100
                data_out['Linear-Langmuir'] = {
                    'ycalc': ycalc_linearlangmuir.tolist(),
                    'params': {k: v for k, v in zip(linearlangmuir.parameter_names, linearlangmuir.parameters)},
                    'aard': aard_linearlangmuir,
                    'xmodel': linearlangmuir.xmodel.tolist(),
                    'ymodel': linearlangmuir.ymodel.tolist()
                }

            if 'bilangmuir' in isotherm_types:
                bilangmuir = isoT.BiLangmuir()
                bilangmuir.fit(x, y)
                ycalc_bilangmuir = bilangmuir.isotherm(x)
                aard_bilangmuir = bilangmuir.aard(ycalc_bilangmuir)*100
                data_out['Bi-Langmuir'] = {
                    'ycalc': ycalc_bilangmuir.tolist(),
                    'params': {k: v for k, v in zip(bilangmuir.parameter_names, bilangmuir.parameters)},
                    'aard': aard_bilangmuir,
                    'xmodel': bilangmuir.xmodel.tolist(),
                    'ymodel': bilangmuir.ymodel.tolist()
                }

            if 'freundlich' in isotherm_types:
                freundlich = isoT.Freundlich()
                freundlich.fit(x, y)
                ycalc_freundlich = freundlich.isotherm(x)
                aard_freundlich = freundlich.aard(ycalc_freundlich)*100
                data_out['Freundlich'] = {
                    'ycalc': ycalc_freundlich.tolist(),
                    'params': {k: v for k, v in zip(freundlich.parameter_names, freundlich.parameters)},
                    'aard': aard_freundlich,
                    'xmodel': freundlich.xmodel.tolist(),
                    'ymodel': freundlich.ymodel.tolist()
                }

            context = {
                'page_title': 'Tools',
                'page_subtitle': 'Programs developed by the EgiChem Group',
                'form': form,
                'data_in': data_in,
                'data_out': data_out,
            }
            return render(request, 'calculators/isotherms.html', context)
    
    else:
        form = IsothermForm()

    context = {
		'page_title': 'Tools',
        'page_subtitle': 'Programs developed by the EgiChem Group',
        'form': form,
	}
    return render(request, 'calculators/isotherms.html', context)