"""
CO2.py
Calculates supercritical carbon dioxide density and viscosity for given temperature and pressure.

Density calculated using the AG-HGK equation
Viscosity calculated using the Altunin-Sakhabetinov empirical expression

"""

import numpy as np


# GLOBAL PARAMETERS
ro_inf_init = 0.001
ro_sup_init = 1.50
perc_er = 1e-6
it_max = 100

# CARBON DIOXIDE CRITICAL CONSTANTS
tttc=304.1       # K
pppc=72.8349174  # atm
vvvc=93.9        # cm3/mol
rrroc=0.4686901  # g/cm3
mmmolwt=44.010   # g/mol

# PARAMETERS OF THE ALTUNIN-SAKHABETINOV
aaa=np.zeros((5,2))
aaa[1][0]= 0.248566120
aaa[1][1]= 0.004894942
aaa[2][0]=-0.373300660
aaa[2][1]= 1.227534880
aaa[3][0]= 0.363854523
aaa[3][1]=-0.774229021
aaa[4][0]=-0.0639070755
aaa[4][1]=0.1425070490

# PARAMETERS OF THE AG-HGK EQUATION
lll=np.zeros(4)
lll[1]=0
lll[2]=2
lll[3]=0
alfaz=np.zeros(4)
alfaz[1]=34
alfaz[2]=40
alfaz[3]=30
betaz=np.zeros(4)
betaz[1]=20000
betaz[2]=20000
betaz[3]=40000
ggg=np.zeros(4)
ggg[1]=-7.53e-4
ggg[2]=-5.73e-3
ggg[3]= 1.84e-4
bbb=np.zeros((10,7))
bbb[0][0]=-0.7255896770
bbb[0][1]=-1.6698566330
bbb[0][2]= 0.4191613578
bbb[0][3]= 1.1540585470
bbb[0][4]= 1.1450275820
bbb[0][5]= 1.1488455130
bbb[0][6]= 0.7069388840
bbb[1][0]= 0.4481451002
bbb[1][1]= 1.2690839330
bbb[1][2]= 6.0578119110
bbb[1][3]= 15.859789780
bbb[1][4]= 20.218370270
bbb[1][5]= 9.1900771440
bbb[2][0]=-0.1743673384
bbb[2][1]=-1.9544044470
bbb[2][2]=-5.6151979650
bbb[2][3]=-6.9768169150
bbb[2][4]=-0.5761694929
bbb[2][5]= 3.0072849370
bbb[3][0]=-4.2438160930e-4
bbb[3][1]=-1.7884558440
bbb[3][2]=-11.346293670
bbb[3][3]=-29.104035620
bbb[3][4]=-30.026639370
bbb[3][5]=-8.3612823860
bbb[4][0]= 0.2668130548
bbb[4][1]= 2.7185742230
bbb[4][2]= 9.4622888160
bbb[4][3]= 10.603173790
bbb[4][4]= 0.1567993789
bbb[4][5]=-2.7232168500
bbb[5][0]= 0.07340283381
bbb[5][1]= 1.1547892190
bbb[5][2]= 7.4509888050
bbb[5][3]= 16.001430470
bbb[5][4]= 10.971048690
bbb[6][0]=-0.1756082074
bbb[6][1]=-2.1141845860
bbb[6][2]=-6.1447687020
bbb[6][3]=-4.6675661180
bbb[7][0]= 8.8442710160e-3
bbb[7][1]= 0.0148894556
bbb[7][2]=-1.4450102070
bbb[7][3]=-1.9979431860
bbb[8][0]= 0.06107749242
bbb[8][1]= 0.6239980516
bbb[8][2]= 1.1940662950
bbb[9][0]=-0.01994277669
bbb[9][1]=-0.1666138543
bbb[9][2]= 5.9238882890e-3


def aghgk(p, t, ro):
    resid=0
    for j in range(0,10):
        for k in range(0,7):
            if bbb[j][k] == 0:
                continue
            else:
                resid+=bbb[j][k]*pow(304.2/t-1,k)*pow(ro/0.468-1,j)
    resid=1+(ro/0.468)*resid

    tau=np.zeros(4)
    tau[1]=tttc/t-1.011
    tau[2]=tttc/t-1.011
    tau[3]=tttc/t-1.009
    delta=(ro-rrroc)/rrroc
    
    for i in range(1,4):
        resid+=(ro/rrroc)*ggg[i]*pow(delta,lll[i]-1)*(lll[i]-2*alfaz[i]*pow(delta,2))*np.exp(-alfaz[i]*pow(delta,2)-betaz[i]*pow(tau[i],2))

    ro_molar=ro/mmmolwt
    resid-=p/ro_molar/t/82.05

    return resid


def get_density(p,t):
    """
    Computes supercritical CO2 density

    INPUTS:
    p : pressure in bar
    t : temperature in celsius

    OUTPUTS:
    ro_inf : supercritical CO2 density at pressure p and temperature t in g/cm3
    """

    # Unit convertion
    p = p/1.01325  # convert bar to atm
    t = t + 273.15  # convert celsius to Kelvin (K)

    ro_inf=ro_inf_init
    ro_sup=ro_sup_init
    res_inf=aghgk(p,t,ro_inf)
    
    for i in range(1,it_max+1):
        ro=(ro_inf+ro_sup)/2
        res=aghgk(p,t,ro)

        if res*res_inf<0:
            ro_sup=ro
        else:
            ro_inf=ro
            res_inf=res

        if (ro_sup-ro_inf)*100/ro_inf <= perc_er:
            break

    return ro_inf


def get_viscosity(t, ro):
    """
    Computes supercritical CO2 viscosity

    INPUTS:
    p : pressure in bar
    ro : temperature in celsius

    OUTPUTS:
    visc : supercritical CO2 viscosity at temperature t in cP
    """

    # Unit convertion
    t = t + 273.15  # convert celsius to Kelvin (K)

    visc=0
    w=ro/0.468
    tau=t/304.2

    for i in range(1,5):
        for j in range(0,2):
            visc += aaa[i][j]*pow(w,i)/pow(tau,j)

    visc = np.exp(visc)
    visc *= (np.sqrt(tau)*(2722.46461-1663.46068/tau+466.920556/tau/tau)*1e-7)

    return visc*10**2


if __name__ == '__main__':
    CO2_dens = get_density(300,60)
    print('CO2 density in g/cm3:', CO2_dens)

    CO2_visc = get_viscosity(60, CO2_dens)
    print('CO2 viscosity in cP:', CO2_visc)