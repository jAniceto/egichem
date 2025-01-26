from feos.pcsaft import PcSaftParameters
from feos.eos import State, EquationOfState, Contributions
import si_units as si
import numpy as np


def get_mole_frac_from_mass_frac(mass_frac, molar_mass):
    """Calculate mole fraction from mass fraction."""
    mole_frac1 = mass_frac[0]/molar_mass[0] / (mass_frac[0]/molar_mass[0] + mass_frac[1]/molar_mass[1])
    mole_frac2 = mass_frac[1]/molar_mass[1] / (mass_frac[0]/molar_mass[0] + mass_frac[1]/molar_mass[1])
    return [mole_frac1, mole_frac2]


def carbon_dioxide(temp, press, cossolvent=None, cossolvent_mol_frac=None, cossolvent_mass_frac=None):
    """Calculate properties of pure SC-CO2 or SC-CO2/EtOH or SC-CO2/MeOH mixtures using PCSAFT EoS.

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
