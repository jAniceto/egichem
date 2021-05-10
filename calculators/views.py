from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CarbonDioxideForm, IsothermForm, PCSAFTForm, GeneralPCSAFTForm

from properties import CO2, CO2_EtOH, EtOH
from properties import isotherms as isoT
from properties import pcsaft_eos
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


def pcsaft_co2(request):
    """Properties of carbon dioxide mixtures using the PC-SAFT equation of state"""
    properties = {
        'molar_density': '',
        'mass_density': '',
        'enthalpy_vaporization': '',
        'residual_enthalpy': '',
        'residual_entropy': '',
        'residual_gibbs': '',
        'fugacity': '',
        'compressibility': '',
        'helmholtz': '',
    }

    if request.method == 'POST':
        form = PCSAFTForm(request.POST)

        if form.is_valid():
            cosolvent = form.cleaned_data['cosolvent']
            temperature = form.cleaned_data['temperature']
            pressure = form.cleaned_data['pressure']
            cosolvent_fraction = form.cleaned_data['cosolvent_fraction']

            if cosolvent == 'NONE':
                system = pcsaft_eos.CarbonDioxide(temperature, pressure)
            elif cosolvent in ['ETHANOL', 'WATER', 'METHANOL']:
                system = pcsaft_eos.CarbonDioxide(
                        temperature, 
                        pressure, 
                        cossolvent=cosolvent.lower(), 
                        cossolvent_fraction=cosolvent_fraction
                    )
            try:
                properties['molar_density'] = f'{system.molar_density():.2f}'
                properties['mass_density'] = f'{system.mass_density():.2f}'
                properties['residual_enthalpy'] = f'{system.residual_enthalpy():.2f}'
                properties['residual_entropy'] = f'{system.residual_entropy():.4f}'
                properties['residual_gibbs'] = f'{system.residual_gibbs():.2f}'
                system_fugacity = system.fugacity()
                properties['fugacity'] = f'{system_fugacity[0]:.4f}'
                if len(system_fugacity) > 1:
                    properties['fugacity_cossolvent'] = f'{system_fugacity[1]:.4f}'
                properties['compressibility'] = f'{system.compressibility():.4f}'
                properties['helmholtz'] = f'{system.helmholtz():.4f}'
            except ValueError as e:
                print(e)
                messages.error(request, 'Invalid input was provided.')
            except:
                messages.error(request, 'PC-SAFT EoS could not be solved.')

            try:
                properties['enthalpy_vaporization'] = f'{system.enthalpy()[0]:.2f}'
            except Exception as e:
                print(e)
                messages.warning(request, 'Warning: Enthalpy of vaporization could not be calculated.')
    else:
        form = PCSAFTForm()

    context = {
		'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
        'form': form,
        'properties': properties,
	}
    return render(request, 'calculators/pcsaft-co2.html', context)


def pcsaft(request):
    """General calculator for the PC-SAFT equation of state"""
    properties = {
        'molar_mass': '',
        'molar_density': '',
        'mass_density': '',
        'enthalpy_vaporization': '',
        'vapor_pressure': '',
        'residual_enthalpy': '',
        'residual_entropy': '',
        'residual_gibbs': '',
        'fugacity': '',
        'compressibility': '',
        'helmholtz': '',
    }

    if request.method == 'POST':
        form = GeneralPCSAFTForm(request.POST)

        if form.is_valid():
            temperature = form.cleaned_data['temperature']
            pressure = form.cleaned_data['pressure']
            molar_fraction_1 = form.cleaned_data['molar_fraction_1']
            molar_mass_1 = form.cleaned_data['molar_mass_1']
            molar_mass_2 = form.cleaned_data['molar_mass_2']
            m_1 = form.cleaned_data['m_1']
            m_2 = form.cleaned_data['m_2']
            s_1 = form.cleaned_data['s_1']
            s_2 = form.cleaned_data['s_2']
            e_1 = form.cleaned_data['e_1']
            e_2 = form.cleaned_data['e_2']
            vol_assoc_1 = form.cleaned_data['vol_assoc_1']
            vol_assoc_2 = form.cleaned_data['vol_assoc_2']
            e_assoc_1 = form.cleaned_data['e_assoc_1']
            e_assoc_2 = form.cleaned_data['e_assoc_2']
            k_12 = form.cleaned_data['k_12']

            try:
                if molar_fraction_1 == 1:
                    system = pcsaft_eos.calculate_properties(
                        temp=temperature, 
                        press=pressure, 
                        x=[molar_fraction_1], 
                        molar_mass=[molar_mass_1], 
                        m=[m_1], 
                        s=[s_1], 
                        e=[e_1], 
                        vol_a=[vol_assoc_1], 
                        e_assoc=[e_assoc_1],
                    )
                else:
                    system = pcsaft_eos.calculate_properties(
                        temp=temperature, 
                        press=pressure, 
                        x=[molar_fraction_1, 1-molar_fraction_1], 
                        molar_mass=[molar_mass_1, molar_mass_2], 
                        m=[m_1, m_2], 
                        s=[s_1, s_2], 
                        e=[e_1, e_2], 
                        vol_a=[vol_assoc_1, vol_assoc_2], 
                        e_assoc=[e_assoc_1, e_assoc_2], 
                        k_ij=[[0., k_12], [k_12, 0.]]
                    )
            except Exception as e:
                print(e)
                messages.error(request, 'PC-SAFT EoS could not be solved.')
                return redirect('pcsaft')
            
            print(system)
            properties['molar_mass'] = f"{system['molar_mass_mix']:.2f}"
            properties['molar_density'] = f"{system['molar_dens']:.2f}"
            properties['mass_density'] = f"{system['mass_dens']:.2f}"
            properties['residual_enthalpy'] = f"{system['residual_enthalpy']:.2f}"
            properties['residual_entropy'] = f"{system['residual_entropy']:.4f}"
            properties['residual_gibbs'] = f"{system['residual_gibbs']:.2f}"
            system_fugacity = system['fugacity']
            properties['fugacity'] = f"{system_fugacity[0]:.4f}"
            if len(system_fugacity) > 1:
                properties['fugacity_cossolvent'] = f"{system_fugacity[1]:.4f}"
            properties['compressibility'] = f"{system['compressibility']:.4f}"
            properties['helmholtz'] = f"{system['helmholtz']:.4f}"

            try:
                properties['enthalpy_vaporization'] = f"{system['enthalpy_vap']:.2f}"
                properties['vapor_pressure'] = f"{system['vap_press']:.2f}"
            except Exception as e:
                print(e)
                messages.warning(request, 'Warning: Enthalpy of vaporization could not be calculated.')
    else:
        form = GeneralPCSAFTForm()

    context = {
		'page_title': PAGE_TITLE,
        'page_subtitle': PAGE_SUBTITLE,
        'form': form,
        'properties': properties,
	}
    return render(request, 'calculators/pcsaft.html', context)