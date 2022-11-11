import csv
import math
import pprint


PROPERTIES = [
    '# atoms', 'Gform', 'Hform', 'Hfusion', 'Hvap', 'Mw', 'Pc', 'Tb', 'Tc',
    'Tm', 'Vc', 'a', 'b', 'c', 'd', 'mua', 'mub'
]

DATA_PATH = 'calculators/static/calculators/data/joback-group-data.csv'


# Load group data from CSV
with open(DATA_PATH, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    group_data = {}
    for row in csv_reader:
        key = row.pop('Group')
        group_data[key] = row


def get_group_list():
    return ['-CH3', '-CH2-', '>CH-', '>C<', '=CH2', '=CH-', '=C<', '=C=', '=-CH', '=-C-', '-CH2- ring', '>CH- ring', '>C< ring', '=CH- ring', '=C< ring', '-F', '-Cl', '-Br', '-I', '-OH alcohol', '-OH phenol', '-O- nonring', '-O- ring', '>C=O nonring', '>C=O ring', 'O=CH- aldehyde', '-COOH acid', '-COO- ester', '=O other than above', '-NH2', '>NH non-ring', '>NH ring', '>N-nonring', '-N= nonring', '-N= ring', '=NH', '-CN', '-NO2', '-SH', '-S- nonring', '-S- ring']


def _sum_group_property(groups, property):
    """Calculate the sum of a property for all functional groups."""
    if property not in PROPERTIES:
        raise ValueError(f'Property must be one of:\n{PROPERTIES}')

    sum_prop = 0
    for group, n in groups.items():
        try:
            sum_prop += (n * float(group_data[group][property]))
        except ValueError as e:
            sum_prop += 0
            print(f"Error found for {group} at {property}.")

    return sum_prop


def molecular_weight(groups):
    """Calculate molecular weight.
    
    .. math:: M_w [g/mol] = \\sum M_{w,i}
    """
    return _sum_group_property(groups, 'Mw')


def normal_boiling_point(groups):
    """Calculate normal boiling point using Joback Method.
    
    .. math:: T_b [K] = 198 + \\sum T_{b,i}
    """
    sum_Tbi = _sum_group_property(groups, 'Tb')
    return 198 + sum_Tbi


def critical_temperature(groups):
    """Calculate critical temperature using Joback Method.
    
    .. math:: T_c [K] = \\frac{T_b}{0.584 + 0.965 \\sum T_{c,i} - (\\sum T_{c,i})^2}
    """
    sum_Tci = _sum_group_property(groups, 'Tc')
    Tb = normal_boiling_point(groups)
    return Tb / (0.584 + 0.965 * sum_Tci - sum_Tci**2)


def critical_pressure(groups):
    """Calculate critical pressure using Joback Method.
    
    .. math:: P_c [bar] = \\left( 0.113 + 0.0032 N_{atom} - \\sum P_{c,i} \\right) ^{-2}
    where :math:`N_{atom}` is the mumber of atoms in the molecule.
    """
    sum_Pci = _sum_group_property(groups, 'Pc')
    sum_atoms = _sum_group_property(groups, '# atoms')
    return (0.113 + 0.0032 * sum_atoms - sum_Pci)**-2


def critical_volume(groups):
    """Calculate critical volume using Joback Method.
    
    .. math:: V_c [cm^3/mol] = 17.5 + \\sum V_{c,i}
    """
    sum_Vci = _sum_group_property(groups, 'Vc')
    return 17.5 + sum_Vci


def critical_compressibility(groups):
    """Calculate critical compressibility using Joback Method.
    
    .. math:: Z_c = \\frac{P_c V_c}{R T_c}
    """
    R = 83.1446261815324  # cm3 bar K−1 mol−1, gas constant
    Pc = critical_pressure(groups)
    Vc = critical_volume(groups)
    Tc = critical_temperature(groups)
    return (Pc * Vc) / (R * Tc)


def acentric_factor(groups):
    """Calculate acentric factor using Lee-Kesler Method.
    .. math:: \\omega = \\alpha / \\beta
    .. math:: \\theta = T_b / T_c
    .. math:: \\alpha = -ln(P_c) - 5.92714 + 6.09648 / \\theta + 1.28862 ln(\\theta) - 0.169347 \\theta^6
    .. math:: \\beta = 15.2518 - 15.6875 / \\theta - 13.4721 ln(\\theta) + 0.43577 \\theta^6
    """
    theta = normal_boiling_point(groups) / critical_temperature(groups)
    Pc = critical_pressure(groups)
    alpha = -math.log(Pc) - 5.92714 + 6.09648 / theta + 1.28862 * math.log(
        theta) - 0.169347 * theta**6
    beta = 15.2518 - 15.6875 / theta - 13.4721 * math.log(
        theta) + 0.43577 * theta**6
    return alpha / beta


def freezing_point(groups):
    """Calculate freezing point.
    .. math:: T_m [K] = 122.5 + \\sum T_{m,i}
    """
    sum_Tmi = _sum_group_property(groups, 'Tm')
    return 122.5 + sum_Tmi


def heat_formation(groups):
    """Calculate heat of formation for ideal gas at 298 K.
    .. math:: H_{form} [KJ/mol] = 122.5 + \\sum H_{form,i}
    """
    sum_Hformi = _sum_group_property(groups, 'Hform')
    return 68.29 + sum_Hformi


def gibbs_formation(groups):
    """Calculate Gibbs energy formation for ideal gas at 298 K.
    .. math:: G_{form} [KJ/mol] = 53.58 + \\sum (G_{form,i} H_{form,i})
    """
    sum_Gformi = _sum_group_property(groups, 'Gform')
    return 53.58 + sum_Gformi


def heat_vaporization_normal(groups):
    """Calculate heat of vaporization at normal boiling point using Reidel's equation.
    .. math:: \\Delta H_v [KJ/mol] = \\frac{1.092 R T_b (ln(P_c) - 1.013)}{0.930 - T_b / T_c}
    """
    R = 0.00831446261815324  # L bar K−1 mol−1, gas constant
    Tb = normal_boiling_point(groups)
    Pc = critical_pressure(groups)
    Tc = critical_temperature(groups)
    return (1.092 * R * Tb * (math.log(Pc) - 1.013)) / (0.930 - Tb / Tc)


def heat_fusion(groups):
    """Calculate heat of fusion.
    .. math:: \\Delta H_{fus} [KJ/mol] = -0.88 + \\sum H_{fus,i}
    """
    sum_Hfusi = _sum_group_property(groups, 'Hfusion')
    return -0.88 + sum_Hfusi


def heat_capacity(groups, temp):
    """Calculate heat of capacity (ideal gas).
    .. math:: C_p [J/(mol K)] = A + B T + C T^2 + D T^3
    .. math:: A = \\sum a_i - 37.93
    .. math:: B = \\sum b_i + 0.210
    .. math:: C = \\sum c_i - 3.91 \\times 10^{-4}
    .. math:: D = \\sum d_i - 2.06 \\times 10^{-7}
    """
    A = _sum_group_property(groups, 'a') - 37.93
    B = _sum_group_property(groups, 'b') + 0.210
    C = _sum_group_property(groups, 'c') - 3.91e-4
    D = _sum_group_property(groups, 'd') + 2.06e-7
    return A + B * temp + C * temp**2 + D * temp**3


def heat_vaporization(groups, temp):
    """Calculate heat of vaporization at given temperature using Watson equation.
    
    .. math:: \\Delta H_{vap} [KJ/mol] = \\Delta H_{vap,ref} \\left( \\frac{T_c - T}{T_c - T_{ref}} \\right) ^{0.38}
    """
    Tc = critical_temperature(groups)
    Tb = normal_boiling_point(groups)
    return heat_vaporization_normal(groups) * ((Tc - temp) / (Tc - Tb))**0.38


def viscosity(groups, temp):
    """Calculate the liquid viscosity.
    
    .. math:: \\mu [Pa \\ s] = M_w e^{A/T + B}
    .. math:: A = \\sum \\mu_a - 597.82
    .. math:: B = \\sum \\mu_b - 11.202
    """
    Mw = molecular_weight(groups)
    A = _sum_group_property(groups, 'mua') - 597.82
    B = _sum_group_property(groups, 'mub') - 11.202
    return Mw * math.exp(A / temp + B)


def density(groups, temp):
    """Calculate the liquid density using Rackett equation.
    .. math:: \\rho [g/cm^3] = \\frac{M_w}{(R T_c / P_c) Z_c^{(1 + (1 - T/T_c)^{2/7})}}
    """
    R = 83.1446261815324  # L bar K−1 mol−1, gas constant
    Tc = critical_temperature(groups)
    Pc = critical_pressure(groups)
    Zc = critical_compressibility(groups)
    Mw = molecular_weight(groups)
    return Mw / ((R * Tc / Pc) * Zc**(1 + (1-temp/Tc)**(2/7)))


def vapor_pressure(groups, temp):
    """Calculate the liquid vapor pressure Lee-Kesler equation.
    .. math:: P_{vap} [bar] = P_c e^{f_0 + w f_1}
    .. math:: T_r = T/T_c
    .. math:: f_0 = 5.92714 - 6.09648/T_r - 1.28862 ln(T_r) + 0.169347 T_r^6
    .. math:: f_1 = 15.2518 - 15.6875/T_r - 13.4721 ln(T_r) + 0.43577 T_r^6
    """
    Pc = critical_pressure(groups)
    w = acentric_factor(groups)
    Tc = critical_temperature(groups)
    Tr = temp / Tc
    f0 = 5.92714 - 6.09648/Tr - 1.28862 * math.log(Tr) + 0.169347 * Tr**6
    f1 = 15.2518 - 15.6875/Tr - 13.4721 * math.log(Tr) + 0.43577 * Tr**6
    return Pc * math.exp(f0 + w * f1)


def joback(groups, temp=None):
    """
    Calculate all available molecule properties using the Joback Method of group
    contributions.
    Parameters
    ----------
    groups : dict
        Dictionary containing the mumber of groups of each type. Key is functional group, 
        value is mumber of occurrences (int) See example below.
    temp : float (optional)
        Specified temperature to return some of the properties [K].
    
    Returns
    -------
    dict
        Dictionary containing calculated properties, units, and description.
    
    Example
    -------
    >>> groups = {
        '-CH3': 1,
        '-CH2-': 3,
        '-OH alcohol': 1,
    }
    >>> res = joback(groups, temp=300)
    >>> print(res['Tc']['value'], res['Tc']['units'], '-', res['Tc']['description'])
    545.080094404856 K - Critical temperature.
    
    References
    ----------
    Chemstation Physical Properties User Guide
    `Wikipedia - Joback method <https://en.wikipedia.org/wiki/Joback_method>`_
    """
    Mw = molecular_weight(groups)
    Tb = normal_boiling_point(groups)
    Tc = critical_temperature(groups)
    Pc = critical_pressure(groups)
    Vc = critical_volume(groups)
    Zc = critical_compressibility(groups)
    w = acentric_factor(groups)
    Tm = freezing_point(groups)
    Hform = heat_formation(groups)
    Gform = gibbs_formation(groups)
    dHvapnorm = heat_vaporization_normal(groups)
    Hfus = heat_fusion(groups)
    if temp:
        Cp = heat_capacity(groups, temp)
        dHvap = heat_vaporization(groups, temp)
        Pvap = vapor_pressure(groups, temp)
        visc = viscosity(groups, temp)
        dens = density(groups, temp)
    else:
        Cp = None
        dHvap = None
        Pvap = None
        visc = None
        dens = None

    return {
        'temp': {'value': temp, 'units': 'K', 'description': 'Specified temperature.'},
        'Mw': {'value': Mw, 'units': 'g/mol', 'description': 'Molecular weight.'},
        'Tb': {'value': Tb, 'units': 'K', 'description': 'Normal boiling point temperature.'},
        'Tc': {'value': Tc, 'units': 'K', 'description': 'Critical temperature.'},
        'Pc': {'value': Pc, 'units': 'bar', 'description': 'Critical pressure.'},
        'Vc': {'value': Vc, 'units': 'cm3/mol', 'description': 'Critical volume.'},
        'Zc': {'value': Zc, 'units': '-', 'description': 'Critical compressibility.'},
        'w': {'value': w, 'units': '-', 'description': 'Acentric factor.'},
        'Tm': {'value': Tm, 'units': 'K', 'description': 'Freezing point temperature.'},
        'Hform': {'value': Hform, 'units': 'KJ/mol', 'description': 'Heat of formation.'},
        'Gform': {'value': Gform, 'units': 'KJ/mol', 'description': 'Gibbs energy of formation.'},
        'dHvapnorm': {'value': dHvapnorm, 'units': 'KJ/mol', 'description': 'Heat of vaporization at normal boiling point.'},
        'Hfus': {'value': Hfus, 'units': 'KJ/mol', 'description': 'Heat of fusion.'},
        'Cp': {'value': Cp, 'units': 'J/(mol K)', 'description': 'Heat capacity.'},
        'dHvap': {'value': dHvap, 'units': 'KJ/mol', 'description': 'Heat of vaporization at the specified temperature.'},
        'visc': {'value': visc, 'units': 'Pa s', 'description': 'Viscosity at the specified temperature.'},
        'dens': {'value': dens, 'units': 'g/cm3', 'description': 'Density at the specified temperature.'},
        'Pvap': {'value': Pvap, 'units': 'bar', 'description': 'Vapor pressure at the specified temperature.'},
    }


if __name__ == '__main__':
    # Example for 1-butanol
    groups = {
        '-CH3': 1,
        '-CH2-': 3,
        '-OH alcohol': 1,
    }
    r = joback(groups, temp=300)
    print(r)
    print(r['Tc']['value'], r['Tc']['units'], '-', r['Tc']['description'])
