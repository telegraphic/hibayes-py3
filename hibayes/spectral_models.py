"""
# spectral_models.py


"""
import os
import sys
import numpy
from numpy import exp, log, sqrt, pi
import pymultinest
from scipy.special import erf
from .priors import Priors
from .profile_support import profile
from .constants import *


@profile
def T_fg(nu_1, c, nc, nu):
    """
    Generate Tf given foreground model coefficients
    T_sky(\nu) = 10^{\sum a_i (log10(\nu/60 MHz))^i}
    """

    exponent = 0.0
    for n in range(nc):
        c_n = c[n]
        exponent += c_n * (numpy.log10(nu / nu_1) ** n)
        #print 'e',nu,nu_1,n,c_n,exponent

    #exponent=c[0]+c[1]*(numpy.log10(nu/nu_1))**1

    Tf = 10 ** exponent
    #Tf = exp(exponent)
    #Tf=exponent
    #print Tf

    return Tf


#-------------------------------------------------------------------------------

@profile
def T_HI(A_HI, nu_HI, sigma_HI, nu, norm=False, erfs=False):
    """
    Units are MHz and ***mK***
    """

    T_HI = A_HI * exp(-(nu - nu_HI) ** 2 / (2.0 * sigma_HI ** 2))
    #T_HI *= 1.0/sqrt(2.0*pi*sigma_HI**2) # Found not required for 100, 67, 5

    #print nu,nu_HI,erfs
    #return T_HI
    if norm: T_HI *= 1.0 / sqrt(2.0 * pi * sigma_HI ** 2)
    if erfs:
        ##    erfs=0.5*(erf((nu_HI-FREQ_MIN)/(sqrtTwo*sigma_HI)) - erf((nu_HI-FREQ_MAX)/(sqrtTwo*sigma_HI))) # !!!! WORKS FOR 100, 67, 5
        #erfs=0.5*(erf(nu_HI/(sqrtTwo*sigma_HI)) + erf((FREQ_MAX-FREQ_MIN-nu_HI)/(sqrtTwo*sigma_HI)))
        erfs = 0.5 * (erf((FREQ_MAX - nu_HI) / (sqrtTwo * sigma_HI)) - erf(
            (FREQ_MIN - nu_HI) / (sqrtTwo * sigma_HI)))  #*sqrt(2.0*pi*sigma_HI**2)
        T_HI *= erfs

    return T_HI
    #return T_HI/erfs
    #return erfs*T_HI # !!!! WORKS FOR 100, 67, 5


#-------------------------------------------------------------------------------

@profile
def sigma(Tsky, B, t):
    """
    Noise model
    Units are K, Hz and sec
    """

    sigma = Tsky / sqrt(B * t)
    #sigma=1.0e-9

    return sigma
