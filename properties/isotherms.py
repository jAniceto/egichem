import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import csv


class Isotherm:
    """
    Base isotherm class with fitting and calculation functions
    """
    def fit(self, xexp, yexp, fobj='ls'):
        """Fit isotherm to experimental data xexp vs yexp"""
        def fobj_ls(param, xexp, yexp):
            """Least-square objective function for isotherm fitting"""
            self.parameters = param
            ycalc = self.isotherm(xexp)
            return np.sum((ycalc - yexp) ** 2)

        def fobj_aard(param, xexp, yexp):
            """Average absolure relative deviation (AARD) objective function for isotherm fitting"""
            self.parameters = param
            ycalc = self.isotherm(xexp)
            return np.sum(np.abs(ycalc - yexp)/yexp)

        if fobj == 'ls':
            param = optimize.fmin(fobj_ls, self.parameters, args=(xexp, yexp,))
        else:
            param = optimize.fmin(fobj_aard, self.parameters, args=(xexp, yexp,))
        
        # Store results and experimental data
        self.parameters  = param
        self.xexp = xexp
        self.yexp = yexp
        
        # Store model
        xrange = np.linspace(0, np.max(self.xexp), 100)
        ycalc = self.isotherm(xrange)
        self.xmodel = xrange
        self.ymodel = ycalc

    def aard(self, ycalc):
        """Calculate average absolure relative deviation (AARD)"""
        if self.yexp[0] == 0:
            yexp = self.yexp[1:]
            ycalc = ycalc[1:]
        else:
            yexp = self.yexp
            ycalc = ycalc
        aards = np.abs(ycalc - yexp)/yexp
        aard = np.sum(aards)/len(aards)
        return aard

    def plot(self, plot_exp=True):
        """Plot isotherm"""
        xrange = np.linspace(0, np.max(self.xexp), 100)
        ycalc = self.isotherm(xrange)
        if plot_exp:
            plt.plot(self.xexp, self.yexp, 'o')
        plt.plot(xrange, ycalc, '-')


class Linear(Isotherm):
    """
    Linear adsorption isotherm
    y = henry * x
    where:
        y : adsorbed amount
        x : concentration in the fluid phase
        henry : linear adsorption constant (Henry constant)
    """
    def __init__(self, henry=0.5):
        self.parameters = [henry]
        self.parameter_names = ['H']

    def isotherm(self, x):
        return self.parameters[0] * x


class Langmuir(Isotherm):
    """
    Langmuir adsorption isotherm
    y = (a * x) / (1 + b * x)
    where:
        y : adsorbed amount
        x : concentration in the fluid phase
        a : Langmuir adsorption constant a
        b : Langmuir adsorption constant b
    """
    def __init__(self, a=2.0, b=0.2):
        self.parameters = [a, b]
        self.parameter_names = ['a', 'b']

    def isotherm(self, x):
        return self.parameters[0] * x / ( 1 + self.parameters[1] * x )


class LinearLangmuir(Isotherm):
    """
    Linear-Langmuir adsorption isotherm
    y = (a * x) / (1 + b * x) + m * x
    where:
        y : adsorbed amount
        x : concentration in the fluid phase
        a : Langmuir adsorption constant a
        b : Langmuir adsorption constant b
        m : Linear adsorption constant
    """
    def __init__(self, a=2.0, b=0.2, m=0.1):
        self.parameters = [a, b, m]
        self.parameter_names = ['a', 'b', 'm']

    def isotherm(self, x):
        return self.parameters[0] * x / ( 1 + self.parameters[1] * x ) + self.parameters[2] * x


class BiLangmuir(Isotherm):
    """
    Bi-Langmuir adsorption isotherm
    y = (a1 * x) / (1 + b1 * x) + (a2 * x) / (1 + b2 * x)
    where:
        y : adsorbed amount
        x : concentration in the fluid phase
        a1 : Langmuir adsorption constant a for site 1
        b1 : Langmuir adsorption constant b for site 1
        a2 : Langmuir adsorption constant a for site 2
        b2 : Langmuir adsorption constant b for site 2
    """
    def __init__(self, a1=2.0, b1=0.2, a2=2.0, b2=0.2):
        self.parameters = [a1, b1, a2, b2]
        self.parameter_names = ['a1', 'b1', 'a2', 'b2']

    def isotherm(self, x):
        return self.parameters[0] * x / ( 1 + self.parameters[1] * x ) + self.parameters[2] * x / ( 1 + self.parameters[3] * x )


class Freundlich(Isotherm):
    """
    Freundlich adsorption isotherm
    y = k * x^(1/n)
    where:
        y : adsorbed amount
        x : concentration in the fluid phase
        k : Freundlich constant k
        n : Freundlich constant n
    """
    def __init__(self, k=0.5, n=0.1):
        self.parameters = [k, n]
        self.parameter_names = ['k', 'n']

    def isotherm(self, x):
        return self.parameters[0] * x**(1/self.parameters[1])


def load_csv(filename):
    """Load csv data into numpy arrays"""
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        data_fields = reader.fieldnames
        x = []
        y = []
        for row in reader:
            x.append(float(row[data_fields[0]]))
            y.append(float(row[data_fields[1]]))
    return np.array(x), np.array(y), data_fields


def load_data(x, y):
    return np.array(x), np.array(y)


if __name__ == '__main__':
    # DATA_FILE = 'data/OA-MIP1-isotherm.csv'
    DATA_FILE = 'data/data2.csv'
    PARAMETER_ESTIMATES = [2, 0.2]
    c_exp, q_exp, data_fields = load_csv(DATA_FILE)

    linear = Linear()
    linear.fit(c_exp, q_exp)
    linear.plot()
    ycalc_linear = linear.isotherm(c_exp)
    print('AARD', linear.aard(ycalc_linear)*100)

    langmuir = Langmuir()
    langmuir.fit(c_exp, q_exp)
    langmuir.plot(plot_exp=False)
    ycalc_langmuir = langmuir.isotherm(c_exp)
    print('AARD', langmuir.aard(ycalc_langmuir)*100)

    lin_langmuir = LinearLangmuir()
    lin_langmuir.fit(c_exp, q_exp)
    lin_langmuir.plot(plot_exp=False)
    ycalc_lin_langmuir = lin_langmuir.isotherm(c_exp)
    print('AARD', lin_langmuir.aard(ycalc_lin_langmuir)*100)

    freundlich = Freundlich()
    freundlich.fit(c_exp, q_exp)
    freundlich.plot(plot_exp=False)
    ycalc_freundlich = freundlich.isotherm(c_exp)
    print('AARD', freundlich.aard(ycalc_freundlich)*100)

    plt.legend(['Experimental', 'Linear', 'Langmuir', 'LinearLangmuir', 'Freundlich'])
    plt.xlabel('C')
    plt.ylabel('q')
    plt.show()
