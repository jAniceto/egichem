import math


def D12pred(T, Density, solvent_Vc, solvent_Tc, solvent_M, solute_Vc, solute_Tc, solute_M, B12, k12):
    # Constants
    Na = 6.0221367e23 #mol-1
    kb = 1.380658e-16 # g cm2 s-2 K
    
    # Calculations
    solvent_dlj = 0.7889e-8*solvent_Vc**(1/3)
    solvent_elj = solvent_Tc/1.2593
    solute_dlj = 0.7889e-8*solute_Vc**(1/3)
    solute_elj = solute_Tc/1.2593

    solute_m = solute_M/Na
    solvent_m = solvent_M/Na

    elj_12 = math.sqrt(solvent_elj*solute_elj)

    T_1_est = T/solvent_elj
    T_2_est = T/solute_elj
    T_12_est = T/elj_12

    dlj_1_eff = 1.1532 * solvent_dlj * (1+ (1.8975*T_1_est)**0.5)**(-1/6)
    dlj_2_eff = 1.1532 * solute_dlj * (1+(1.8975*T_2_est)**0.5)**(-1/6)

    densd1 = Density*Na/solvent_M
    density_est = densd1*dlj_1_eff**3

    compress_1 = math.pi/6*density_est

    m12 = solute_m*solvent_m/(solute_m+solvent_m)

    g_sig_est_12 = 1/(1-compress_1)**3*(1-compress_1+2*compress_1/(1+dlj_1_eff/dlj_2_eff))*(1-compress_1+compress_1/(1+dlj_1_eff/dlj_2_eff))

    a = -1.676382*density_est + 1.638561
    b = -8.516830*density_est + 8.631536
    c = -1.320347*density_est + 1.351067
    d = -5.062546*density_est + 5.409662

    F11 = 1 + 0.94605*density_est**1.5 + 1.4022*density_est**3 - 5.6898*density_est**5 + 2.6626*density_est**7
    F12 = (F11 + density_est**1.7* (a*math.log(dlj_2_eff/dlj_1_eff) + b*math.log(dlj_2_eff/dlj_1_eff)**2 + c*math.log(solute_m/solvent_m) ) )/(1 + density_est**3*(d*math.log(dlj_2_eff/dlj_1_eff))**2)

    if F11 < 0:
        raise ValueError('F11 is out of bounds, F11 must be >= 0')

    if F12 < 0:
        raise ValueError('F12 is out of bounds, F12 must be >= 0')
    
    dlj_12_P2 = (1-k12)*(solvent_dlj + solute_dlj)/2
    dlj_12_eff_P2 = 1.1532*dlj_12_P2*(1+(1.8975*T_12_est)**0.5)**(-1/6)

    D12calc1_HS = kb*T
    D12calc2_P2 = 8/3*densd1*dlj_12_eff_P2**2
    D12calc3_P2 = math.sqrt(2*math.pi*kb*T*m12)
    D12calc4_P2 = g_sig_est_12/F12+(B12)/(T_12_est**1.5)
    D12calc = D12calc1_HS/(D12calc2_P2*D12calc3_P2*D12calc4_P2)
    return D12calc


def main():
    # Teste 1 Cyclohexane/Argon
    T = 298.15
    Density = 0.774
    solvent_Vc = 308.0 
    solvent_Tc = 553.50
    solvent_M = 84.162
    solute_Vc = 74.90
    solute_Tc = 150.80
    solute_M = 39.948
    B12 = -4.148463743
    k12 = -0.949757372718528
    print("D12 = {:1.3e}".format(D12pred(T, Density, solvent_Vc, solvent_Tc, solvent_M, solute_Vc, solute_Tc, solute_M, B12, k12)))

    # Teste 2 ACT/Co2
    T = 308.2
    Density = 0.386904957
    solvent_Vc = 93.9
    solvent_Tc = 304.1
    solvent_M = 44.01
    solute_Vc = 209
    solute_Tc = 508.1
    solute_M = 58.08

    B12 = 0.328224648
    k12 = 0.045529293
    print("D12 = {:1.3e}".format(D12pred(T, Density, solvent_Vc, solvent_Tc, solvent_M, solute_Vc, solute_Tc, solute_M, B12, k12)))

    # Teste 3 error
    T = 308.2
    Density = 0.386904957
    solvent_Vc = 93.9
    solvent_Tc = 304.1
    solvent_M = 44.01
    solute_Vc = 209
    solute_Tc = 508.1
    solute_M = 58.08

    B12 = 0.328224648
    k12 = 0.045529293
    print("D12 = {:1.3e}".format(D12pred(T, Density, solvent_Vc, solvent_Tc, solvent_M, solute_Vc, solute_Tc, solute_M, B12, k12)))


if __name__ == '__main__':
    main()
