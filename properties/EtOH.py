"""
EtOH.py
Calculates ethanol density and viscosity for given temperature and pressure.

Density calculated using the Tait equation: 
M.J. Assael, J.H. Dymond, S.K. Polimatidou, Int J Thermophys 15 (1994) 189.
https://link.springer.com/article/10.1007/BF01441581#citeas

Viscosity calculated using the Mamedov equation
J.J. Cano-Gómez, G.A. Iglesias-Silva, M. Ramos-Estrada, Correlations for the prediction of the density and viscosity of 1-alcohols at high pressures, Fluid Phase Equilibria 404 (2015) 109-117.
https://www.sciencedirect.com/science/article/pii/S0378381215300157
"""

import numpy as np


# Supercritical properties
Tc = 513.92  # K 
P0 = 0.101  # MPa

# Density equation constants
Cn = 2
a0 = 1.87961
a1 = -0.55029
a2 = -0.11935
a3 = -0.00161
a4 = 0.01344
a5 = 13.54426
a6 = -4.3235e-4
a7 = 9.54e-6
a8 = 2.20e-6
a =	0.72719
b =	-0.39294
d =	0.47272
c =	-0.89255
Cx = 0.2

# Viscosity equation constants
Aq = -6.4406
Bq = 1.1176e3
Cq = 1.3721e-2
Dq = -1.5465e-5


def get_density_viscosity(P, T):
    """
    Computes ethanol density and viscosity

    INPUTS: 
    P : pressure in bar
    T : temperature in celsius

    OUTPUTS:
    density : ethanol density at pressure p and temperature t in g/cm3
    visc : supercritical CO2 viscosity at temperature t in cP
    """
    PM = P * 0.1
    K = a+b*np.exp(c*Cn**d)
    nD = a0+a1*Cn**a2+a3*Cn+a4/(Cn**a5)+(a6+a7*Cn**0.5+a8*Cn**0.75)*T
    Dens0 = ((nD**2-1)/(nD+0.4))*1/K

    Tr = (T+273.15)/Tc
    F = 0.015*Cn*(1+11.5*Cn)
    B = 520.23 - 1240*Tr + 827*Tr**2 - F
    dens = Cx*np.log((B+PM)/(B+P0))*Dens0 + Dens0

    visc0 = 10**(Aq+Bq/(T+273.15)+Cq*(T+273.15)+Dq*(T+273.15)**2)
    Ax = 10.4+0.0006*Cn**3.5-5/Cn
    visc = visc0*(dens/Dens0)**Ax

    return dens, visc


if __name__ == '__main__':
    d, v = get_density_viscosity(300, 60)

    print('Density', d, 'g/cm3')
    print('Viscosity', v, 'cp')
