import numpy as np
import pcsaft


class CarbonDioxide():
    """
    Calculate physio and thermodynamic properties of carbon dioxide and
    carbon dioxide/cossolvent mixtures using the PC-SAFT Equation of State.

    Parameters
    ----------
    temperature : float
        Temperature [ºC].
    pressure : float
        Pressure [bar].
    cossolvent : string, optional
        The cossolvent of carbon dioxide. 
    cossolvent_fraction : float, optional
        Molar fraction of the cossolvent [mol/mol].
    """
    def __init__(self, temperature, pressure, cossolvent=None, cossolvent_fraction=0.):
        self.temperature = temperature + 273.15  # Celsius to Kelvin
        self.pressure = pressure * 1e5  # bar to Pascal
        self.cossolvent = cossolvent
        self.cossolvent_fraction = cossolvent_fraction
        self.x = np.asarray([1-cossolvent_fraction, cossolvent_fraction])  # mol/mol, molar fractions

        if cossolvent == None:
            # CO2 PC-SAFT parameters
            # CO2 - component 1
            m = np.asarray([2.0729])
            s = np.asarray([2.7852])
            e = np.asarray([169.21]) 
            self.x = np.asarray([1.])
            self.pcsaft_parameters = {'m':m, 's':s, 'e':e}
            molar_mass = np.asarray([44.01])  # g/mol
            self.molar_mass_mix = self.x[0]*molar_mass[0]

        elif cossolvent == 'ethanol':
            # CO2-Ethanol PC-SAFT parameters
            # CO2 - component 1
            # Ethanol - component 2
            m = np.asarray([2.0729, 2.3827])
            s = np.asarray([2.7852, 3.1771])
            e = np.asarray([169.21, 198.24]) 
            k_ij = np.asarray([[0., 0.], [0., 0.]]) 
            vol_a = np.asarray([0, 0.032384])
            e_assoc = np.asarray([0, 2653.4])
            self.pcsaft_parameters = {'m':m, 's':s, 'e':e, 'k_ij':k_ij, 'vol_a': vol_a, 'e_assoc': e_assoc}
            molar_mass = np.asarray([44.01, 46.07])  # g/mol
            self.molar_mass_mix = self.x[0]*molar_mass[0] + self.x[1]*molar_mass[1]

        elif cossolvent == 'water':
            # CO2-Water PC-SAFT parameters
            # CO2 - component 1
            # Water - component 2
            m = np.asarray([2.0729, 1.0656])
            s = np.asarray([2.7852, 3.0007])
            e = np.asarray([169.21, 366.51]) 
            k_ij = np.asarray([[0., 0], [0, 0.]]) 
            vol_a = np.asarray([0, 0.034868])
            e_assoc = np.asarray([0, 2500.7])
            self.pcsaft_parameters = {'m':m, 's':s, 'e':e, 'k_ij':k_ij, 'vol_a': vol_a, 'e_assoc': e_assoc}
            molar_mass = np.asarray([44.01, 18.01528])  # g/mol
            self.molar_mass_mix = self.x[0]*molar_mass[0] + self.x[1]*molar_mass[1]

        elif cossolvent == 'methanol':
            # CO2-Methanol PC-SAFT parameters
            # CO2 - component 1
            # Methanol - component 2
            m = np.asarray([2.0729, 1.5255])
            s = np.asarray([2.7852, 3.23])
            e = np.asarray([169.21, 188.9]) 
            k_ij = np.asarray([[0., 0.018285945], [0.018285945, 0.]]) 
            vol_a = np.asarray([0, 0.035176])
            e_assoc = np.asarray([0, 2899.5])
            self.pcsaft_parameters = {'m':m, 's':s, 'e':e, 'k_ij':k_ij, 'vol_a': vol_a, 'e_assoc': e_assoc}
            molar_mass = np.asarray([44.01, 32.04])  # g/mol
            self.molar_mass_mix = self.x[0]*molar_mass[0] + self.x[1]*molar_mass[1]

        else:
            raise ValueError(f'Cossolvent "{cossolvent}" is not supported. Supported cossolvents are "ethanol", "methanol" and "water".')

        self._validate_inputs()

    def _validate_inputs(self):
        """Validate inputs."""
        # Validate molar fraction input
        if (self.cossolvent_fraction > 1.) or (self.cossolvent_fraction < 0.):
            raise ValueError('The molar fraction of the cossolvent must be in the range [0, 1].')
        if (self.cossolvent is not None) and (self.cossolvent_fraction == 0.):
            raise ValueError('The cossolvent molar fraction cannot be 0 if a cossolvent is specified.')

    def molar_density(self):
        """Calculate the molar density.
        
        Returns
        -------
        self.molar_dens : float
            Molar density of the mixture [mol/m3]
        """
        self.molar_dens = pcsaft.pcsaft_den(self.temperature, self.pressure, self.x, self.pcsaft_parameters)
        return self.molar_dens

    def mass_density(self):
        """Calculate the mass density.
        
        Returns
        -------
        float
            Mass density of the mixture [kg/m3]
        """
        self.molar_density()
        return self.molar_dens * self.molar_mass_mix / 1000

    def enthalpy(self):
        """Calculate the enthalpy of vaporization.
        
        Returns
        -------
        list [float, float]
            0: enthalpy of vaporization [J/mol]
            1: vapor pressure [Pa]
        """
        return pcsaft.pcsaft_Hvap(self.temperature, self.x, self.pcsaft_parameters)

    def residual_enthalpy(self):
        """Calculate the residual enthalpy for one phase of the system.
        
        Returns
        -------
        float
            Residual enthalpy [J/mol]
        """
        return pcsaft.pcsaft_hres(self.temperature, self.molar_dens, self.x, self.pcsaft_parameters)

    def residual_entropy(self):
        """Calculate the residual entropy (constant volume) for one phase of the system.
        
        Returns
        -------
        float
            Residual entropy [J/mol/K]
        """
        return pcsaft.pcsaft_sres(self.temperature, self.molar_dens, self.x, self.pcsaft_parameters)

    def residual_gibbs(self):
        """Calculate the residual Gibbs energy for one phase of the system.
        
        Returns
        -------
        float
            Residual Gibbs energy [J/mol]
        """
        return pcsaft.pcsaft_gres(self.temperature, self.molar_dens, self.x, self.pcsaft_parameters)

    def fugacity(self):
        """Calculate the fugacity coefficients for one phase of the system.
        
        Returns
        -------
        ndarray, shape (n,)
            Fugacity coefficients of each component.
        """
        return pcsaft.pcsaft_fugcoef(self.temperature, self.molar_dens, self.x, self.pcsaft_parameters)

    def compressibility(self):
        """Calculate the compressibility factor.
        
        Returns
        -------
        float
            Compressibility factor
        """
        return pcsaft.pcsaft_Z(self.temperature, self.molar_dens, self.x, self.pcsaft_parameters)

    def helmholtz(self):
        """Calculate the residual Helmholtz energy.
        
        Returns
        -------
        float
            Residual Helmholtz energy [J/mol]
        """
        return pcsaft.pcsaft_ares(self.temperature, self.molar_dens, self.x, self.pcsaft_parameters)


if __name__ == '__main__':
    # co2_EtOH = CarbonDioxide(30, 50, cossolvent='ethanol', cossolvent_fraction=0.15)
    # print('molar density', co2_EtOH.molar_density())
    # print('mass density', co2_EtOH.mass_density())
    # print('enthalpy vaporization', co2_EtOH.enthalpy())
    # print('res enthalpy', co2_EtOH.residual_enthalpy())
    # print('res entropy', co2_EtOH.residual_entropy())
    # print('res gibbs', co2_EtOH.residual_gibbs())
    # print('fugacity', co2_EtOH.fugacity())
    # print('compress', co2_EtOH.compressibility())
    # print('helmholtz', co2_EtOH.helmholtz())

    co2 = CarbonDioxide(20, 1)
    print('molar density', co2.molar_density())
    print('mass density', co2.mass_density())
    print('enthalpy vaporization', co2.enthalpy())
    print('res enthalpy', co2.residual_enthalpy())
    print('res entropy', co2.residual_entropy())
    print('res gibbs', co2.residual_gibbs())
    print('fugacity', co2.fugacity())
    print('compress', co2.compressibility())
    print('helmholtz', co2.helmholtz())

