"""
CO2_EtOH.py
Calculates supercritical carbon dioxide / ethanol mixture density for given temperature and pressure.
"""

import numpy as np
from scipy import optimize


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


if __name__ == '__main__':
    print(get_density(300, 60, 0.1))
