# -*- coding: utf-8 -*-
"""
Created on Wed July 13 2016

@author: fangren
"""


import numpy as np
import matplotlib.pyplot as plt
import imp
from scipy import interpolate

plotTernary = imp.load_source("plt_ternary_save", "plotTernary_prediction.py")



path = 'C:\Research_FangRen\Data\Metallic_glasses_data\CoVZr_ternary\Logan_prediction\\'
save_path = path + 'plots\\'


alloy = 'Co VZr'


filename_new = path + 'new-glasses_' + alloy + '.csv'
data_new = np.genfromtxt(filename_new, delimiter=',', skip_header = 1)

metal1_new = data_new[:,3]*100
metal2_new = data_new[:,4]*100
metal3_new = data_new[:,5]*100
probability_new = data_new[:, 1]


filename_old = path + 'old-model_' + alloy + '.csv'
data_old = np.genfromtxt(filename_old, delimiter=',', skip_header = 1)

metal1_old = data_old[:,3]*100
metal2_old = data_old[:,4]*100
metal3_old = data_old[:,5]*100
probability_old = data_old[:, 1]

if (metal1_new == metal1_old).all() and (metal2_new == metal2_old).all() and (metal3_new == metal3_old).all():
    ternary_data = np.concatenate(([metal1_old],[metal2_old],[metal3_old],[probability_old]), axis = 0)
    ternary_data = np.transpose(ternary_data)

    plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=(alloy[0:2], alloy[2:4], alloy[4:6]), scale=100,
                           sv=True, svpth=save_path, svflnm= alloy + '_old_model.png',
                           cbl='Scale', vmin = 0.5, vmax = 1, cmap='viridis_r', cb=True, style='h')

    ternary_data = np.concatenate(([metal1_old],[metal2_old],[metal3_old],[probability_new]), axis = 0)
    ternary_data = np.transpose(ternary_data)

    plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=(alloy[0:2], alloy[2:4], alloy[4:6]), scale=100,
                           sv=True, svpth=save_path, svflnm= alloy + '_new_model.png',
                           cbl='Scale', vmin = 0, vmax = 1, cmap='viridis_r', cb=True, style='h')


    # interpolation
    probability_func_old = interpolate.Rbf(metal1_old, metal2_old, metal3_old, probability_old, function='multiquadric',
                                           smooth=0.3)
    probability_func_new = interpolate.Rbf(metal1_old, metal2_old, metal3_old, probability_new, function='multiquadric',
                                           smooth=0.3)



    metal1_range = np.arange(0, 100, 1.5)
    metal2_range = np.arange(0, 100, 1.5)

    metal1 = []
    metal2 = []
    metal3 = []

    probability_interpolate_old = []
    probability_interpolate_new = []

    for i in metal1_range:
        for j in metal2_range:
            if i + j <= 100 and i+j >= 0:
                try:
                    metal1.append(i)
                    metal2.append(j)
                    metal3.append(100-i-j)
                    probability_interpolate_old.append(float(probability_func_old(i, j, (100-i-j))))
                    probability_interpolate_new.append(float(probability_func_new(i, j, (100-i-j))))
                except(ValueError):
                    continue


    ternary_data = np.concatenate(([metal1],[metal2],[metal3],[probability_interpolate_old]), axis = 0)
    ternary_data = np.transpose(ternary_data)

    plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=(alloy[0:2], alloy[2:4], alloy[4:6]), scale=100,
                           sv=True, svpth=save_path, svflnm=alloy + '_interpolate_old_model.png',
                           cbl='Scale', vmin = 0, vmax = 1, cmap='viridis_r', cb=True, style='h')

    ternary_data = np.concatenate(([metal1],[metal2],[metal3],[probability_interpolate_new]), axis = 0)
    ternary_data = np.transpose(ternary_data)

    plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=(alloy[0:2], alloy[2:4], alloy[4:6]), scale=100,
                           sv=True, svpth=save_path, svflnm=alloy + '_interpolate_new_model.png',
                           cbl='Scale', vmin = 0, vmax = 1, cmap='viridis_r', cb=True, style='h')

    probability_interpolate_new = np.array(probability_interpolate_new)
    probability_interpolate_old = np.array(probability_interpolate_old)
    ternary_data = np.concatenate(([metal1],[metal2],[metal3],[probability_interpolate_new-probability_interpolate_old]), axis = 0)
    ternary_data = np.transpose(ternary_data)

    plotTernary.plt_ternary_save(ternary_data, tertitle='',  labelNames=(alloy[0:2], alloy[2:4], alloy[4:6]), scale=100,
                           sv=True, svpth=save_path, svflnm=alloy + '_interpolate_difference.png',
                           cbl='Scale', cmap='viridis_r', cb=True, style='h')

    plt.close("all")


