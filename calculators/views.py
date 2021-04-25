from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CarbonDioxideForm, IsothermForm

from properties import CO2, CO2_EtOH, EtOH
from properties import isotherms as isoT
import numpy as np

# Globals
PAGE_TITLE = 'Tools'
PAGE_SUBTITLE = 'Online calculators developed by the EgiChem Group'


def calculators_home(request):
    """Online calculators homepage"""
    context = {
		'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
	}
    return render(request, 'calculators/calculators_home.html', context)


def carbon_dioxide(request):
    """Carbon dioxide properties calculator"""
    if request.method == 'POST':
        form = CarbonDioxideForm(request.POST)

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
                density_si = f'{CO2_dens*1000:.4f}'  # convert g/cm3 to kg/m3
                viscosity_si = f'{CO2_visc*0.001:.4E}'  # convert cP to Pa s
            
            elif cosolvent == 'ETHANOL':
                # Calculate pure CO2-EtOH density and viscosity
                CO2EtOH_dens = CO2_EtOH.get_density(pressure, temperature, cosolvent_fraction)
                CO2EtOH_visc = CO2_EtOH.get_viscosity(pressure, temperature, cosolvent_fraction)
                density = f'{CO2EtOH_dens:.8f}'
                viscosity = f'{CO2EtOH_visc:.8f}'
                density_si = f'{CO2EtOH_dens*1000:.4f}'  # convert g/cm3 to kg/m3
                viscosity_si = f'{CO2EtOH_visc*0.001:.4E}'  # convert cP to Pa s

        else:
            density = ''
            viscosity = ''
            density_si = ''
            viscosity_si = ''
    
    else:
        form = CarbonDioxideForm()
        density = ''
        viscosity = ''
        density_si = ''
        viscosity_si = ''

    context = {
		'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
        'form': form,
        'density': density,
        'viscosity': viscosity,
        'density_si': density_si,
        'viscosity_si': viscosity_si
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
    """Adsorption isotherm fitting calculator"""
    if request.method == 'POST':
        form = IsothermForm(request.POST)

        if form.is_valid():
            xy_data = form.cleaned_data['xy_data']
            isotherm_types = form.cleaned_data['isotherm_type']
            
            try:
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
                    r_square_linear = linear.R_square(ycalc_linear)
                    r_square_adjusted_linear = linear.R_square_adjusted(ycalc_linear, 1)
                    data_out['Linear'] = {
                        'ycalc': ycalc_linear.tolist(),
                        'params': {k: v for k, v in zip(linear.parameter_names, linear.parameters)},
                        'aard': aard_linear,
                        'r_square': r_square_linear,
                        'r_square_adjusted': r_square_adjusted_linear,
                        'xmodel': linear.xmodel.tolist(),
                        'ymodel': linear.ymodel.tolist()
                    }

                if 'langmuir' in isotherm_types:
                    langmuir = isoT.Langmuir()
                    langmuir.fit(x, y)
                    ycalc_langmuir = langmuir.isotherm(x)
                    aard_langmuir = langmuir.aard(ycalc_langmuir)*100
                    r_square_langmuir = langmuir.R_square(ycalc_langmuir)
                    r_square_adjusted_langmuir = langmuir.R_square_adjusted(ycalc_langmuir, 2)
                    data_out['Langmuir'] = {
                        'ycalc': ycalc_langmuir.tolist(),
                        'params': {k: v for k, v in zip(langmuir.parameter_names, langmuir.parameters)},
                        'aard': aard_langmuir,
                        'r_square': r_square_langmuir,
                        'r_square_adjusted': r_square_adjusted_langmuir,
                        'xmodel': langmuir.xmodel.tolist(),
                        'ymodel': langmuir.ymodel.tolist()
                    }

                if 'linearlangmuir' in isotherm_types:
                    linearlangmuir = isoT.LinearLangmuir()
                    linearlangmuir.fit(x, y)
                    ycalc_linearlangmuir = linearlangmuir.isotherm(x)
                    aard_linearlangmuir = linearlangmuir.aard(ycalc_linearlangmuir)*100
                    r_square_linearlangmuir = linearlangmuir.R_square(ycalc_linearlangmuir)
                    r_square_adjusted_linearlangmuir = linearlangmuir.R_square_adjusted(ycalc_linearlangmuir, 3)
                    data_out['Linear-Langmuir'] = {
                        'ycalc': ycalc_linearlangmuir.tolist(),
                        'params': {k: v for k, v in zip(linearlangmuir.parameter_names, linearlangmuir.parameters)},
                        'aard': aard_linearlangmuir,
                        'r_square': r_square_linearlangmuir,
                        'r_square_adjusted': r_square_adjusted_linearlangmuir,
                        'xmodel': linearlangmuir.xmodel.tolist(),
                        'ymodel': linearlangmuir.ymodel.tolist()
                    }

                if 'bilangmuir' in isotherm_types:
                    bilangmuir = isoT.BiLangmuir()
                    bilangmuir.fit(x, y)
                    ycalc_bilangmuir = bilangmuir.isotherm(x)
                    aard_bilangmuir = bilangmuir.aard(ycalc_bilangmuir)*100
                    r_square_bilangmuir = bilangmuir.R_square(ycalc_bilangmuir)
                    r_square_adjusted_bilangmuir = bilangmuir.R_square_adjusted(ycalc_bilangmuir, 4)
                    data_out['Bi-Langmuir'] = {
                        'ycalc': ycalc_bilangmuir.tolist(),
                        'params': {k: v for k, v in zip(bilangmuir.parameter_names, bilangmuir.parameters)},
                        'aard': aard_bilangmuir,
                        'r_square': r_square_bilangmuir,
                        'r_square_adjusted': r_square_adjusted_bilangmuir,
                        'xmodel': bilangmuir.xmodel.tolist(),
                        'ymodel': bilangmuir.ymodel.tolist()
                    }

                if 'freundlich' in isotherm_types:
                    freundlich = isoT.Freundlich()
                    freundlich.fit(x, y)
                    ycalc_freundlich = freundlich.isotherm(x)
                    aard_freundlich = freundlich.aard(ycalc_freundlich)*100
                    r_square_freundlich = freundlich.R_square(ycalc_freundlich)
                    r_square_adjusted_freundlich = freundlich.R_square_adjusted(ycalc_freundlich, 2)
                    data_out['Freundlich'] = {
                        'ycalc': ycalc_freundlich.tolist(),
                        'params': {k: v for k, v in zip(freundlich.parameter_names, freundlich.parameters)},
                        'aard': aard_freundlich,
                        'r_square': r_square_freundlich,
                        'r_square_adjusted': r_square_adjusted_freundlich,
                        'xmodel': freundlich.xmodel.tolist(),
                        'ymodel': freundlich.ymodel.tolist()
                    }

                context = {
                    'page_title': PAGE_TITLE,
                    'page_subtitle': PAGE_SUBTITLE,
                    'form': form,
                    'data_in': data_in,
                    'data_out': data_out,
                }
                return render(request, 'calculators/isotherms.html', context)
            
            except:
                # If isotherm fitting fails, redirect to calculator and show error message
                messages.error(request, 'Isotherm fitting failed. Try clicking "Example data" to see ao data should be submitted.')
                return redirect('isotherms')

    
    else:
        form = IsothermForm()

    context = {
		'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
        'form': form,
	}
    return render(request, 'calculators/isotherms.html', context)


def d12_sc_co2(request):
    """Prediction of binary diffusivities in supercritical carbon dioxide using ML"""
    context = {
        'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
    }
    return render(request, 'calculators/d12_sc_co2.html', context)


def d12_polar_nonpolar(request):
    """Prediction of binary diffusivities in polar and nonpolar systems using ML"""
    context = {
        'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
    }
    return render(request, 'calculators/d12_polar_nonpolar.html', context)


def psychrometrics(request):
    """Psychrometric functions to calculate thermodynamic properties of air"""
    context = {
        'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
    }
    return render(request, 'calculators/psychrometrics.html', context)


def psychrometrics_ventilation(request):
    """Psychrometric functions to calculate thermodynamic properties of air"""
    context = {
        'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
    }
    return render(request, 'calculators/psychrometrics_vent.html', context)


def unit_conversion(request):
    """Unit conversions"""
    context = {
        'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
    }
    return render(request, 'calculators/unit_conversion.html', context)


def air_properties(request):
    """Properties of dry air at atmospheric pressure"""
    context = {
        'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
    }
    return render(request, 'calculators/air_properties.html', context)
