from feos.pcsaft import Identifier, PcSaftRecord, PureRecord, PcSaftParameters
from feos.eos import State, EquationOfState, Contributions
import si_units as si
import numpy as np


def get_mole_frac_from_mass_frac(mass_frac, molar_mass):
    """Calculate mole fraction from mass fraction."""
    mole_frac1 = mass_frac[0]/molar_mass[0] / (mass_frac[0]/molar_mass[0] + mass_frac[1]/molar_mass[1])
    mole_frac2 = mass_frac[1]/molar_mass[1] / (mass_frac[0]/molar_mass[0] + mass_frac[1]/molar_mass[1])
    return [mole_frac1, mole_frac2]


def carbon_dioxide(temp, press, cossolvent=None, cossolvent_mol_frac=None, cossolvent_mass_frac=None):
    """Calculate properties of pure SC-CO2 or SC-CO2/EtOH or SC-CO2/MeOH mixtures using PC-SAFT EoS.

    Arguments:
        temp (float) : temperature in Kelvin
        press (float) : pressure in bar
        cossolvent (string) : name of the cossolvent (either ethanol or methanol). Default is None meaning pure CO2 (no cossolvent).
        cossolvent_mol_frac (float) : mole franction of the cossolvent in the mixture. Either this of cossolvent_mass_frac 
                                      must be provided if cossolvent is not None.
        cossolvent_mass_frac (float) : mass franction of the cossolvent in the mixture. Either this of cossolvent_mol_frac 
                                       must be provided if cossolvent is not None.

    Returns:
        dict : dictionary containing several calculated properties.
    """
    # PC-SAFT parameters data
    file_na = 'properties/data/esper2023.json'  # single component parameters
    file_binary = 'properties/data/rehner2023_binary.json'  # binary interaction parameters

    # Molar masses
    MW = {
        'carbon dioxide': 44.010,  # g/mol
        'ethanol': 46.069,  # g/mol
        'methanol': 32.042,  # g/mol
    }

    valid_cossolvents = ['ethanol', 'methanol']
    
    if cossolvent is None:
        # Pure CO2
        parameters = PcSaftParameters.from_json(['carbon dioxide'], pure_path=str(file_na))

        pcsaft = EquationOfState.pcsaft(parameters)
        state = State(
            pcsaft,
            temperature=temp*si.KELVIN,
            pressure=press*si.BAR
        )
    
    elif cossolvent in valid_cossolvents:
        # CO2/cossolvent mixture
        if cossolvent_mass_frac:
            mole_fracs = get_mole_frac_from_mass_frac([1-cossolvent_mass_frac, cossolvent_mass_frac], [MW['carbon dioxide'], MW[cossolvent]])
            mole_fracs = np.array(mole_fracs)

        elif cossolvent_mol_frac:
            mole_fracs = np.array([1-cossolvent_mol_frac, cossolvent_mol_frac])

        else:
            raise Exception('If a cossolvent is selected either cossolvent_mol_frac or cossolvent_mass_frac must be provided.')
        
        parameters = PcSaftParameters.from_multiple_json([(['carbon dioxide', cossolvent], str(file_na))], binary_path=str(file_binary))

        pcsaft = EquationOfState.pcsaft(parameters)
        state = State(
            pcsaft,
            temperature=temp*si.KELVIN,
            pressure=press*si.BAR,
            molefracs=mole_fracs
        )
    
    else:
        raise Exception('Invalid cossolvent selected. Cossolvent must be either None, ethanol, or methanol.')
    
    # Results    
    return {
        'molar_density': state.density / si.MOL * si.METER**3,  # mol/m3
        'mass_density': state.mass_density() / si.KILOGRAM * si.METER**3,  # kg/m3
        'residual_enthalpy': state.molar_enthalpy(Contributions.Residual) / si.JOULE * si.MOL,  # J/mol
        'residual_entropy': state.molar_entropy(Contributions.Residual) / si.JOULE * si.MOL * si.KELVIN,  # J/mol/K
        'helmholtz_energy': state.molar_helmholtz_energy(Contributions.Residual) / si.JOULE * si.MOL,  # J/mol
        'compressibility': state.compressibility(Contributions.Residual), 
    }


def pure_or_binary(temp, press, mw, mol_fracs=None, m=None, sigma=None, epsilon_k=None, kappa_ab=None, epsilon_k_ab=None, na=None, nb=None, nc=None, k_ij=None):
    """Calculate properties of pure substance or binary mixture using PC-SAFT EoS.

    Arguments:
        temp (float) : temperature in Kelvin
        press (float) : pressure in bar
        mw (float | list) : molecular weight for each substance
        mol_fracs (float | list) : mol fractions for each substance
        m (float | list) : PC-SAFT parameter for each substance
        sigma (float | list) : PC-SAFT parameter for each substance
        epsilon_k (float | list) : PC-SAFT parameter for each substance
        kappa_ab (float | list) : PC-SAFT parameter for each substance
        epsilon_k_ab (float | list) : PC-SAFT parameter for each substance
        na (float | list) : PC-SAFT parameter for each substance
        nb (float | list) : PC-SAFT parameter for each substance
        nc (float | list) : PC-SAFT parameter for each substance
        k_ij (float | list) : PC-SAFT parameter for each substance

    Returns:
        dict : dictionary containing several calculated properties.
    """
    if isinstance(mw, float):
        # Pure compound
        # Create pure compound record from the identifier and PC-SAFT record
        comp1 = PureRecord(
            Identifier(name='comp1'), 
            molarweight=mw, 
            model_record=PcSaftRecord(
                m=m, 
                sigma=sigma, 
                epsilon_k=epsilon_k,
                kappa_ab=kappa_ab, 
                epsilon_k_ab=epsilon_k_ab, 
                na=na, nb=nb, nc=nc
            )
        )

        # Build PC-SAFT parameters for a pure compound
        parameters = PcSaftParameters.new_pure(comp1)

        # Calculate properties
        pcsaft = EquationOfState.pcsaft(parameters)
        state = State(
            pcsaft,
            temperature=temp*si.KELVIN,
            pressure=press*si.BAR,
        )

    elif isinstance(mw, list):
        # Binary mixture
        if not kappa_ab:
            kappa_ab = [None, None]
        if not epsilon_k_ab:
            epsilon_k_ab = [None, None]
        if not na:
            na = [None, None]
        if not nb:
            nb = [None, None]
        if not nc:
            nc = [None, None]
        
        # Create pure compound record from each mixture component using an identifier and PC-SAFT record
        comp0 = PureRecord(
            Identifier(name='comp0'), 
            molarweight=mw[0], 
            model_record=PcSaftRecord(
                m=m[0], 
                sigma=sigma[0], 
                epsilon_k=epsilon_k[0],
                kappa_ab=kappa_ab[0], 
                epsilon_k_ab=epsilon_k_ab[0], 
                na=na[0], nb=nb[0], nc=nc[0]
            )
        )
        comp1 = PureRecord(
            Identifier(name='comp1'), 
            molarweight=mw[1], 
            model_record=PcSaftRecord(
                m=m[1], 
                sigma=sigma[1], 
                epsilon_k=epsilon_k[1],
                kappa_ab=kappa_ab[1], 
                epsilon_k_ab=epsilon_k_ab[1], 
                na=na[1], nb=nb[1], nc=nc[1]
            )
        )
        
        # Build PC-SAFT parameters for a binary mixture
        parameters = PcSaftParameters.new_binary([comp0, comp1], binary_record=k_ij)

        # Calculate properties
        pcsaft = EquationOfState.pcsaft(parameters)
        state = State(
            pcsaft,
            temperature=temp*si.KELVIN,
            pressure=press*si.BAR,
            molefracs=np.array(mol_fracs)
        )
    else:
        raise Exception('PC-SAFT parameters like mw must be a float (for pure components) or list (for binary mixtures).')

    return {
        'molar_density': state.density / si.MOL * si.METER**3,  # mol/m3
        'mass_density': state.mass_density() / si.KILOGRAM * si.METER**3,  # kg/m3
        'residual_enthalpy': state.molar_enthalpy(Contributions.Residual) / si.JOULE * si.MOL,  # J/mol
        'residual_entropy': state.molar_entropy(Contributions.Residual) / si.JOULE * si.MOL * si.KELVIN,  # J/mol/K
        'helmholtz_energy': state.molar_helmholtz_energy(Contributions.Residual) / si.JOULE * si.MOL,  # J/mol
        'compressibility': state.compressibility(Contributions.Residual), 
    }
