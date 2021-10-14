import numpy as np
from scipy import special, optimize


def _clean_data(yexp, ycalc):
    """Remove zeros from experimental data (yexp) so it can be safely used to
    in calculations (e.g., to calculate AARD). Remove the corresponding point in
    calculated data (ycalc).

    Parameters
    ----------
    yexp : array
        Experimental values.
    ycalc : array
        Calculated values.

    Returns
    -------
    numpy.array
        Cleaned experimental values.
    numpy.array
        Cleaned calculated values.
    """
    cleaned_yexp, cleaned_ycalc = [], []
    for exp, calc in zip(yexp, ycalc):
        if exp == 0:
            continue
        cleaned_yexp.append(exp)
        cleaned_ycalc.append(calc)
    return np.array(cleaned_yexp), np.array(cleaned_ycalc)


def _aard(yexp, ycalc):
    """Calculate average absolute relative deviation (AARD).

    .. math::  AARD (\\%) = \\frac{100}{NDP} \\sum_{i=1}^{NDP} \\left| \\frac{y^{calc} - y^{exp}}{y^{exp}} \\right|_i

    Parameters
    ----------
    yexp : numpy.array
        Experimental values.
    ycalc : numpy.array
        Calculated values.

    Returns
    -------
    aard : float
        Average absolute relative deviation (AARD) [%].
    """
    yexp, ycalc = _clean_data(yexp, ycalc)
    aards = np.abs(ycalc - yexp) / yexp
    aard = np.sum(aards) / len(aards) * 100
    return aard


def _r_square(yexp, ycalc):
    """Calculate determination coefficient (R^2).

    Parameters
    ----------
    yexp : numpy.array
        Experimental values.
    ycalc : numpy.array
        Calculated values.

    Returns
    -------
    r_square : float
        Determination coefficient.
    """
    yavg = np.mean(yexp)
    r_square = 1 - (np.sum((yexp - ycalc)**2)) / (np.sum((yexp - yavg)**2))
    return r_square


def _r_square_adjusted(yexp, ycalc, n_param):
    """Calculate adjusted determination coefficient.

    Parameters
    ----------
    yexp : numpy.array
        Experimental values.
    ycalc : numpy.array
        Calculated values.
    n_param : int
        Number of model parameters.

    Returns
    -------
    r_square_adjusted : float
        Adjusted determination coefficient.
    """
    n = len(ycalc)
    r_square = _r_square(yexp, ycalc)
    r_square_adjusted = 1 - (1 - r_square) * (n - 1) / (n - n_param - 1)
    return r_square_adjusted


class Klinkenberg:
    """Klinkenberg model.

    Klinkenberg provides an useful approximation to the analytical solution of
    the Convection-Dispersion model proposed by Anzelius for the case of a
    single solute, an initially clean bed, frontal loading and negligible axial
    dispersion. According to the Klinkenberg approximation the solute
    concentration respect to axial distance and time is given by:

    .. math::  \\frac{C}{C_F} \\approx \\frac{1}{2} [ 1 + \\text{erf}( \\sqrt{\\tau} - \\sqrt{\\xi} + \\frac{1}{8 \\sqrt{\\tau}} + \\frac{1}{8 \\sqrt{\\xi}} ) ]

    .. math::  \\tau = K (t - \\frac{z}{u_i})

    .. math::  \\xi = \\frac{K H z}{u_i} (\\frac{1 - \\varepsilon_b}{\\varepsilon_b})

    Parameters
    ----------
    H : float
        Linear adsorption constant (also called Henry constant).
    K : float
        Convective mass transfer coefficient.
    z : float
        Axial distance.
    ui : float
        Interstitial velocity.
    epsilonb : float
        Bulk porosity.

    Attributes
    ----------
    t_model : numpy.array
        Range of values time values in the Klinkenberg model.
    C_model : numpy.array
        Range of values for the concentration in the fluid using the Klinkenberg
        model.
    metrics : dict
        Fitting metrics of the the Klinkenberg model fitted to experimental
        data. Contains the average absolute relative deviation, R squared, and
        R squared adjusted metrics.

    References
    ----------
    A. Klinkenberg, Ind. Eng. Chem., 46, 2285–2289 (1954).

    J.D. Seader, E.J. Henley, D.K. Roper. Separation Process Principles.
    John Wiley & Sons, Inc., 3rd edition, 2011.
    """
    def __init__(self, H=None, K=None, z=None, ui=None, epsilonb=None):
        self.H = H
        self.K = K
        self.z = z
        self.ui = ui
        self.epsilonb = epsilonb

    def model(self, t, Cfeed=1.0):
        """Klinkenberg model function.

        Parameters
        ----------
        t : numpy.array
            Time coordinate.
        Cfeed : float, optional
            Feed concentration for each set of experimental data. Defaults to 1.0.

        Returns
        -------
        numpy.array
            Concentration in the fluid phase. E.g., [mol/L].
        """
        if not (self.H and self.K and self.ui and self.z and self.epsilonb):
            raise ValueError('Model parameters must be defined.')

        xi = self.K * self.H * self.z / self.ui * (1 - self.epsilonb) / self.epsilonb
        tau = self.K * (t - self.z / self.ui)
        return Cfeed / 2 * (1 + special.erf(tau**0.5 - xi**0.5 + 1/(8*tau**0.5) + 1/(xi**0.5)))

    def fit(self, t_exp, C_exp, Cfeed=1.0, H_guess=None, K_guess=None, fobj='ls'):
        """Fit chromatographic model to experimental data.

        Parameters
        ----------
        t_exp : numpy.array
            Time. E.g., [min].
        C_exp : numpy.array
            Concentration in the fluid phase. E.g., [mg/mL].
        Cfeed : float, optional
            Feed concentration for each set of experimental data. Defaults to 1.0.
        H_guess : float, optional
            Initial guess for the optimization of the linear adsorption constant.
        K_guess : float, optional
            Initial guess for the optimization of the convective mass transfer coefficient.
        fobj : string, optional
            Objective function to use in fitting. Either 'ls' or 'aard'.
            'ls': least-squares objective function.
            'aard': average absolute relative deviation objective function.

        Returns
        -------
        numpy.array
            Time coordinate for the Klinkenberg model.
        numpy.array
            Concentration in the fluid phase for the Klinkenberg model.
        """
        def fobj_ls(param, x, y, feed):
            """Least-square objective function for isotherm fitting"""
            self.H = param[0]
            self.K = param[1]
            return np.sum((self.model(x, feed) - y) ** 2)

        def fobj_aard(param, x, y):
            """Average absolute relative deviation (AARD) objective function
            for isotherm fitting"""
            self.H = param[0]
            self.K = param[1]
            C_calc = self.model(x)
            return np.sum(np.abs(C_calc - y) / y)

        if H_guess and K_guess:
            parameters = [H_guess, K_guess]
        elif self.H and self.K:
            parameters = [self.H, self.K]
        else:
            raise ValueError('Initial guesses for H and K must be provided for fitting.')

        if fobj == 'ls':
            param = optimize.fmin(fobj_ls, parameters, args=(t_exp, C_exp, Cfeed,))
        else:
            param = optimize.fmin(fobj_aard, parameters, args=(t_exp, C_exp, Cfeed,))

        self.H = param[0]
        self.K = param[1]
        self.t_model = np.linspace(0, np.max(t_exp), 100)
        self.C_model = self.model(self.t_model, Cfeed)
        C_calc = self.model(t_exp, Cfeed)
        self.metrics = {
            'aard': _aard(C_exp, C_calc),
            'r_square': _r_square(C_exp, C_calc),
            'r_square_adjusted': _r_square_adjusted(C_exp, C_calc, len(param)),
        }
        return self.t_model, self.C_model

    def fit_multiple(self, t_exp, C_exp, Cfeed=None, H_guess=None, K_guess=None, fobj='ls'):
        """Fit chromatographic model to several sets of experimental data.

        Parameters
        ----------
        t_exp : list of numpy.array
            Time. E.g., [min].
        C_exp : list of numpy.array
            Concentration in the fluid phase. E.g., [mg/mL].
        Cfeed : list of float, optional
            Feed concentration for each set of experimental data. Defaults to 1.0.
        H_guess : float, optional
            Initial guess for the optimization of the linear adsorption constant .
        K_guess : float, optional
            Initial guess for the optimization of the convective mass transfer coefficient.
        fobj : string, optional
            Objective function to use in fitting. Either 'ls' or 'aard'.
            'ls': least-squares objective function.
            'aard': average absolute relative deviation objective function.

        Returns
        -------
        numpy.array
            Time coordinate for the Klinkenberg model.
        numpy.array
            Concentration in the fluid phase for the Klinkenberg model.
        """
        def fobj_multiple_ls(param, t_list, C_list, Cfeed_list):
            """Least-square objective function for isotherm fitting"""
            self.H = param[0]
            self.K = param[1]
            errors = []
            for time, conc, conc_feed in zip(t_list, C_list, Cfeed_list):
                errors.append(np.sum((self.model(time, conc_feed) - conc) ** 2))
            return np.sum(errors)

        def fobj_multiple_aard(param, x, y):
            """Average absolute relative deviation (AARD) objective function
            for isotherm fitting"""
            self.H = param[0]
            self.K = param[1]
            C_calc = self.model(x)
            return np.sum(np.abs(C_calc - y) / y)

        if H_guess and K_guess:
            parameters = [H_guess, K_guess]
        elif self.H and self.K:
            parameters = [self.H, self.K]
        else:
            raise ValueError('Initial guesses for H and K must be provided for fitting.')

        nc = len(t_exp)
        if not Cfeed:
            Cfeed = [1.0] * nc

        if fobj == 'ls':
            param = optimize.fmin(fobj_multiple_ls, parameters, args=(t_exp, C_exp, Cfeed,))
        else:
            param = optimize.fmin(fobj_multiple_aard, parameters, args=(t_exp, C_exp, Cfeed,))
        
        self.H = param[0]
        self.K = param[1]
        self.t_model = []
        self.C_model = []
        C_calc = []
        for t_, cexp_, cfeed_ in zip(t_exp, C_exp, Cfeed):
            # Create a time vector for each set of data
            t_model_ = np.linspace(0, np.max(t_), 100)
            self.t_model.append(t_model_)
            # Create the model curve for each set of data
            C_model_ = self.model(t_model_, cfeed_)
            self.C_model.append(C_model_)
            # Calculate the model values for each experimental time for each set of data
            C_calc_ = self.model(t_, cfeed_)
            C_calc.append(C_calc_)
        
        # Calculate metrics
        aard, r_square, r_square_adjusted = [], [], []
        for exp, calc in zip(C_exp, C_calc):
            aard.append(_aard(exp, calc))
            r_square.append(_r_square(exp, calc))
            r_square_adjusted.append(_r_square_adjusted(exp, calc, len(param)))
        self.metrics = {
            'aard': aard,
            'r_square': r_square,
            'r_square_adjusted': r_square_adjusted,
        }
        return self.t_model, self.C_model

    def get_parameters(self):
        """Get the model parameters.

        Returns
        -------
        dict
            Dictionary of model parameters.
        """
        return {
            'K': self.K,
            'H': self.H
        }
