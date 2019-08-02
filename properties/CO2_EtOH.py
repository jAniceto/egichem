"""
CO2_EtOH.py
Calculates supercritical carbon dioxide / ethanol mixture density for given temperature and pressure.

Density calculated using the Soave-Redlich-Kwong equation of state
M. Kariznovi, H. Nourozieh, J. Abedi, Experimental measurements and predictions of density, viscosity, and carbon dioxide solubility in methanol, ethanol, and 1-propanol, The Journal of Chemical Thermodynamics, 57 (2013) 408-415. 
https://www.sciencedirect.com/science/article/pii/S0021961412003801

Viscosity calculated using the Kendall and Monroe mixing relation
J. Kendall, K.P. Monroe, The viscosity of liquids. II. The viscosity composition curve for ideal liquid mixtures, Journal of the American Chemical Society  39-9 (1917) 1787-1802.
https://pubs.acs.org/doi/abs/10.1021/ja02254a001
"""

import numpy as np
from scipy import optimize
from properties import EtOH
from properties import CO2


# Properties of CO2 and Ethanol
M1 = 44.010  # g/mol, molar mass of component 1
M2 = 46.069  # g/mol, molar mass of component 2
delta_12 = 0.0789
omega_a = 0.42747
omega_b = 0.08664 
Rg = 8.314462  # MPa.cm3.mol-1.K-1
Tc1 = 304.12  # K
Tc2 = 513.92  # K 
Pc1 = 7.374  # MPa 
Pc2 = 6.148  # MPa
Vc1 = 94.07  # cm3/mol
Vc2 = 167.00  # cm3/mol
w1 = 0.225
w2 = 0.649
Vm0 = 50


def SRK(Vm, x2, T, P):
    x1=1-x2
    b1 = omega_b*Rg*Tc1/Pc1
    b2 = omega_b*Rg*Tc2/Pc2
    k1 = 0.480+1.574*w1-0.176*w1**2
    k2 = 0.480+1.574*w2-0.176*w2**2
    alpha1 = (1+k1*(1-(T/Tc1)**(1/2)))**2
    alpha2 = (1+k2*(1-(T/Tc2)**(1/2)))**2
    a1 = omega_a*Rg**2*Tc1**2/Pc1*alpha1
    a2 = omega_a*Rg**2*Tc2**2/Pc2*alpha2
    D1 =np.sqrt(a1)*(x1*np.sqrt(a1)+x2*(1-delta_12)*np.sqrt(a2))
    D2 = np.sqrt(a2)*(x2*np.sqrt(a2)+x1*(1-delta_12)*np.sqrt(a1))
    am = (1-x2)*D1+x2*D2
    bm = (1-x2)*b1+x2*b2
    Pcalc = (Rg*T)/(Vm-bm)-am/(Vm**2+Vm*bm)
    return (P-Pcalc)**2


def get_density(P, T, x2):
    """
    Computes supercritical CO2-EtOH density

    INPUTS: 
    P : pressure in bar
    T : temperature in celsius
    x2 : molar fraction of solvent 2

    OUTPUTS:
    density : supercritical CO2-EtOH density at pressure p and temperature t in g/cm3
    """
    P = P * 0.1  # convert P from bar to MPa
    T = T + 273.15  # convert T from ºC to K
    minimum, fopt, iterations, funcalls, warnflag = optimize.fmin(SRK, Vm0, args=(x2, T, P,), full_output=True)

    if warnflag == 0:
        mr = M1*(1-x2) + M2*x2
        density = 1/minimum[0]*mr
        return density
    else:
        print(f'Optimization failed with warning flag {warnflag}.')
        return None


def get_viscosity(P, T, x2):
    """
    Computes supercritical CO2 viscosity

    INPUTS:
    p : pressure in bar
    T : temperature in celsius
    x2 : molar fraction of solvent 2

    OUTPUTS:
    visc : supercritical CO2 viscosity at temperature t in cP
    """
    dens_EtOH, visc_EtOH = EtOH.get_density_viscosity(P, T)
    dens_CO2 = CO2.get_density(P, T)
    visc_CO2 = CO2.get_viscosity(T, dens_CO2)

    visc_mix = ( x2 * visc_EtOH**(1/3) + (1-x2) * visc_CO2**(1/3) )**3

    return visc_mix


if __name__ == '__main__':
    print('Density', get_density(275, 30, 0.08))
    print('Viscosity', get_viscosity(275, 30, 0.08))
