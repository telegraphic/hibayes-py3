"""
#sky_model.py

Basic sky model for low-freq observations
"""

import os
import numpy
import pylab as plt
from .profile_support import profile
from .spectral_models import T_HI, T_fg, sigma

#-------------------------------------------------------------------------------

@profile
def generate_simulated_data(rp, plot_data=False):
    """ Generate simulated data of antenna temperature spectrum measurement

    Args:
        rp (dict): Runtime parameter dictionary, as generated by parse_config()
        plot_data (bool): Plot the simulated data.

    Returns:
        (Tmeas, freqs): tuple of simulated temperature-frequency pairs
    """
    # Set up the simulated data
    freqs = numpy.arange(rp["FREQ_MIN"], rp["FREQ_MAX"], rp["BW"]/1.0e6)
    Tmeas = numpy.zeros(len(freqs))
    Tpure = numpy.zeros(len(freqs))
    draw = numpy.zeros(len(freqs))
    Thi = numpy.zeros(len(freqs))
    numpy.random.seed(seed=rp["seed_SIM"])
    Tall = numpy.zeros((len(freqs), 6))

    if True:
        global c,nc,nu_1
        c=rp["coeffs"]
        nc=rp["ncoeffs"]
        nu_1=rp["nu_1"]

    for idatum in range(len(freqs)):
        Thi[idatum] = 1.0e-3 * T_HI(rp["A_HI_TRUE"], rp["NU_HI_TRUE"], rp["SIGMA_HI_TRUE"], freqs[idatum])
        Tpure[idatum] = 1.0e-3 * T_HI(rp["A_HI_TRUE"], rp["NU_HI_TRUE"],
                                      rp["SIGMA_HI_TRUE"], freqs[idatum]) + T_fg(nu_1, c, nc, freqs[idatum])
        draw[idatum] = numpy.random.normal(0.0, sigma(Tpure[idatum], rp["BW"], rp["tObs"]), 1)
        Tmeas[idatum] = Tpure[idatum] + draw[idatum]
        #print idatum,freqs[idatum],T_HI(-100.0,67.0,5.0,freqs[idatum]),
        #print Tf(nu_1,c,nc,freqs[idatum]),Tpure,Tmeas[idatum]
        #print idatum, freqs[idatum], Tpure[idatum], Tmeas[idatum]
        Tall[idatum, :] = [freqs[idatum], Tpure[idatum], draw[idatum], Tmeas[idatum], T_fg(nu_1, c, nc, freqs[idatum]),
                           Thi[idatum]]

    if not os.path.exists(rp["outdir"]): os.mkdir(rp["outdir"])
    #    numpy.savetxt('tall.txt',Tall,header='freq Tpure noise Tmeas Tf T_HI')
    numpy.savetxt(os.path.join(rp["outdir"], 'tpure.txt'), Tpure)
    numpy.savetxt(os.path.join(rp["outdir"], 'tmeas.txt'), Tmeas)
    numpy.savetxt(os.path.join(rp["outdir"], 'tnoise.txt'), draw)
    numpy.savetxt(os.path.join(rp["outdir"], 'thi.txt'), Thi)


    if plot_data:
        plt_titles = ["Model data (foreground + HI)", "Simulated data (with noise)", "noise", "T_HI"]
        plt.figure("simulated_data")

        for ii, data in enumerate([Tpure, Tmeas, draw, Thi]):
            plt.subplot(2, 2, ii + 1)
            plt.title(plt_titles[ii])
            plt.plot(freqs, data)
            plt.xlabel("Frequency (MHz")
            plt.ylabel("Temperature [K]")
        plt.tight_layout()
        plt.show()

    return Tmeas, freqs

#-------------------------------------------------------------------------------
