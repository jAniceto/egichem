"""
Classic models for the calculation of diffusivities (D12)

Author: José Aniceto
"""

def wilke_chang(temp, visc, vol_crit, molar_mass, phi=1):
    """Calculate D12 using the Wilke-Chang model.

    The Wilke-Chang equation is an empirical modification of the Stokes-Einstein relation and is given by:

    .. math::
        D_{12} = 7.4 \times 10^{-8} \frac{(\phi M_1)^{0.5} T}{\mu_1 (V_{Tc,bp,2})^0.6}
        V_{Tc,bp,2} = 0.285 \times V_{c,2})^1.048

    where subscripts 1 and 2 represent solvent and solute, respectively, M1 is the molar mass of solvent, 
    μ1 is the viscosity of the solvent, T is the temperature, ϕ is the association factor of the solvent, 
    Vc,2 is the critical volume of the solute, and VTc,bp,2 is the solute molar volume at normal boiling temperature.

    Parameters
    ----------
    temp : float
        Temperature (K)
    visc : float
        Viscosity of the solvent (cp)
    vol_crit : float
        Critical volume of the solute (cm3/mol)
    molar_mass : float
        Molar mass of solvent (g/mol)
    phi : float
        Association factor of the solvent (nondimensional). 
        For water phi is 2.26, for methanol is 1.9, for ethanol 1.5, and for nonassociated solvents it is 1.

    Returns
    -------
    float
        Diffusivity (cm2/s)
    """
    Vtc = 0.285 * vol_crit**1.048
    return (7.4e-8 * (phi*molar_mass)**0.5 * temp) / (visc * Vtc**0.6)
    

def lai_tan(temp, visc, vol_crit, molar_mass):
    """Calculate D12 using the Lai-Tan model.

    The Lai-Tan equation is a modification of the Wilke-Chang equation specifically devised for diffusion 
    coefficients in supercritical carbon dioxide.

    .. math::
        D_{12} = 2.50 \times 10^{-7} \frac{M_1^{0.5} T}{(10 \times \mu_1)^0.688 (V_{c,2})^0.284}
        
    Where subscripts 1 and 2 represent solvent and solute, respectively, M1 is the molar mass of solvent, 
    μ1 is the viscosity of the solvent, T is the temperature, and Vc,2 is the critical volume of the solute.

    Parameters
    ----------
    temp : float
        Temperature (K)
    visc : float
        Viscosity of the solvent (cp)
    vol_crit : float
        Critical volume of the solute (cm3/mol)
    molar_mass : float
        Molar mass of solvent (g/mol)

    Returns
    -------
    float
        Diffusivity (cm2/s)
    """
    return (2.5e-7 * (molar_mass)**0.5 * temp) / ((10 * visc)**0.688 * vol_crit**(0.284))


def tyn_calus(temp, visc, Vbp1, Vbp2):
    """Calculate D12 using the Tyn-Calus model.

    The Tyn-Calus model is hydrodynamic equation, which is described by:

    .. math::
        D_{12} = 8.94 \times 10^{-8} \frac{V_{bp,1}^0.267}{V_{bp,2}^0.433} \frac{T}{\mu_1}
        
    Where subscripts 1 and 2 represent solvent and solute, respectively, Vbp is the molar volume 
    at normal boiling temperature, μ1 is the viscosity of the solvent, and T is the temperature.

    Parameters
    ----------
    temp : float
        Temperature (K)
    visc : float
        Viscosity of the solvent (cp)
    Vbp1 : float
        molar volume of the solvent at normal boiling temperature (cm3/mol)
    Vbp2 : float
        molar volume of the solute at normal boiling temperature (cm3/mol)

    Returns
    -------
    float
        Diffusivity (cm2/s)
    """
    return 8.94e-8 * Vbp1**0.267 / Vbp2**0.433 * temp / visc


def dhb(temp, Bdhb, V1, Vd):
    """Calculate D12 using the Dymond-Hildebrand-Batschinski (DHB) model.

    The DHB model is a free-volume based model frequently adopted to describe transport 
    properties in nonpolar systems.

    .. math::
        D_{12} = B_{DHB} \sqrt{T} (V_1 - V_D)
        
    Where subscripts 1 and 2 represent solvent and solute, respectively, V1 is the molar mass of solvent, 
    μ1 is the viscosity of the solvent, T is the temperature, and Vc,2 is the critical volume of the solute.

    Parameters
    ----------
    temp : float
        Temperature (K)
    Bdhb : float
        A DHB parameter characteristic of the solute-solvent pair (cm3 mol-1 K-0.5)
    V1 : float
        Molar volume of the solvent (cm3/mol)
    Vd : float
        Minimum solvent molar volume required for diffusion (cm3/mol)

    Returns
    -------
    float
        Diffusivity (cm2/s)
    """
    return Bdhb * temp**0.5 * (V1-Vd)