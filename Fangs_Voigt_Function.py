# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 15:37:51 2016

@author: fangren
"""

import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from os.path import basename
from scipy.optimize import curve_fit
# import imp
# peakdet = imp.load_source("peakdet", "peak_detection.py")
    

def func(x, *params):
    """
    create a Lorentzian fitted curve according to params
    """
    y = np.zeros_like(x)
    for i in range(0, len(params), 4):
        ctr = params[i]
        amp = params[i+1]
        wid = params[i+2]
        n = params[i+3]
        y = y + n * amp * np.exp( -4 * np.log(2) * ((x - ctr)/wid)**2) + (1-n) * amp * wid**2 / 4 / ((x-ctr)**2 + wid**2 / 4)

        '''
        CHANGES

        ORIGINAL EQUATION
        linear_comb = n * amp * np.exp( -((x - ctr)/sigma)**2) + (1-n) * amp * gamma**2 / ((x-ctr)**2 + gamma**2)

        GAUSSIAN
        sigma = wid / (2 * sqrt(2 * ln 2))

        LORENZIAN
        gamma = wid / 2

        FINAL EQUAITON
        n * amp * np.exp( -4 * np.log(2) * ((x - ctr)/wid)**2) + (1-n) * amp * wid**2 / 4 / ((x-ctr)**2 + wid**2 / 4)

        '''


    return y

path = 'D:\\SLAC\Experiments\\Co-Fe-V-Zr Metallic Glasses\\Fang Data (Dropbox)\\1D_spectra_files\\background_subtracted\\'
save_path = path + 'peak_fit_Voigt\\'
if not os.path.exists(save_path):
    os.makedirs(save_path)

guess = [3.9, 100, 0.3, 0.5, 3.1, 5000, 0.33, 0.5]
high = [4.0, 175, 0.5, 1, 3.4, 10000, 0.8, 1]
low = [3.8, 75, 0.1, 0, 2.1, 0, 0, 0]

print(glob.glob(path + '*.csv'))

for filename in glob.glob(path + 'Sample14\\*.csv'):
    print(filename)
    if basename(filename)[-5] == 'd':
        print('processing', filename)
        data = np.genfromtxt(filename, delimiter = ',' )
        Qlist = data[:,0][:647]
        IntAve = data[:,1][:647]
        try:
            data = np.genfromtxt(filename, delimiter = ',' )
            Qlist = data[:,0][:647]
            IntAve = data[:,1][:647]
            
            popt, pcov = curve_fit(func, Qlist, IntAve, p0=guess, bounds = (low, high))
            fit = func(Qlist, *popt)
            plt.figure(1)            
            plt.plot(Qlist, IntAve)
            plt.plot( Qlist, fit)
            ctr1 = popt[0]
            amp1 = popt[1]
            wid1 = popt[2]
            n1 = popt[3]
            ctr2 = popt[4]
            amp2 = popt[5]
            wid2 = popt[6]
            n2 = popt[7]
            curve1 = n1 * amp1 * np.exp( -4*np.log(2)*((Qlist - ctr1)/wid1)**2) + (1-n1) * amp1 * wid1**2 / (4*(Qlist-ctr1)**2 + wid1**2)
            curve2 = n2 * amp2 * np.exp( -4*np.log(2)*((Qlist - ctr2)/wid2)**2) + (1-n2) * amp2 * wid2**2 / (4*(Qlist-ctr2)**2 + wid2**2)

            plt.plot(Qlist, curve1)
            plt.plot(Qlist, curve2)

            plt.show()
            plt.savefig(save_path + basename(filename)[:-4] + '_peak_analysis_Voigt')
            plt.close()
            
            popt = np.reshape(popt, (popt.size/4, 4))
            np.savetxt(save_path + basename(filename)[:-4] + '_peak_analysis_Voigt.csv', popt, delimiter=",")
            
        except RuntimeError:
            np.savetxt(save_path + basename(filename)[:-4] + '_peak_analysis_Voigt.csv', popt, delimiter=",")
            
    exit()