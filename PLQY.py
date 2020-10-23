#!/usr/bin/env python3
# 2020 Wei-Kai Lee

# coding=utf-8
# -*- coding: utf8 -*-

# python module
import sys, os
import os

# third party module
import numpy as np 
from scipy import interpolate
import pandas as pd

#
# A1 : activation light wavelength range measurement when there is no sample in the integrating sphere
# B1 : activation light wavelength range measurement when sample is in the sphere but light does not hit on the sample
# B2 :   emission light wavelength range measurement when sample is in the sphere but light does not hit on the sample
# C1 : activation light wavelength range measurement when sample is in the sphere and light         hits on the sample
# C2 :   emission light wavelength range measurement when sample is in the sphere and light         hits on the sample
#
measuredFilenameList = ('A1.txt','B1.txt','C1.txt','B2.txt','C2.txt') 
def read_CFfile( filepath='./data', filename='CF.txt' ):
    return pd.read_csv( os.path.join(filepath, filename), sep='\t', header=None )
def PLQY_calculator( filepath, CF_pd, exciting_range=(315, 335), emission_range=(400, 720), filenameList = measuredFilenameList):

    # interpolation object
    CF_fun = interpolate.interp1d(CF_pd.values[:,0], CF_pd.values[:,1], bounds_error=True)

    # prepare container
    int_value_list = np.zeros( (len(filenameList),), dtype=np.float )

    # read file 
    for ii, fname in enumerate(filenameList):
        data_pd = pd.read_csv( os.path.join(filepath,fname), sep=r"\s+|;|:|\t",header=None, engine='python' )
        wv, intensity = data_pd.values[:,0], data_pd.values[:,1]

        if ii in (0,1,2): # for A1/B1/C1
            index = np.logical_and( wv>=exciting_range[0], wv<=exciting_range[1] )
        else:
            index = np.logical_and( wv>exciting_range[1], np.logical_and( wv>=emission_range[0], wv<=emission_range[1] ) )

        # select wavelength
        wv, intensity = wv[index], intensity[index]

        # calibrate
        intensity = intensity * CF_fun(wv) * wv

        # integrate
        int_value_list[ii] = np.trapz( y=intensity, x=wv)

    A = 1 - int_value_list[2]/int_value_list[1] # 1-C1/B1
    PLQY = ( int_value_list[4] - (1-A)*int_value_list[3] ) / ( int_value_list[0]*A )
    return A, PLQY
def printSummary(A_array, PLQY_array):
    A_array, PLQY_array = np.array(A_array), np.array(PLQY_array)
    data_size = A_array.size
    print('========================== Summary =========================')
    print( ' '.join( ['{0:>15s}'.format( 'Absorption : ' )] + [ '{0:6.1f}%'.format(A_array[ii]*100) for ii in range(data_size) ] ) )
    print( '{0:>15s} {1:>6.1f}% {2:>15s} {3:>6.1f}% '.format( 'Ave. : ', np.mean(A_array)*100, 'Std. : ', np.std(A_array)*100) )
    print( ' '.join( ['{0:>15s}'.format( 'Quantum Yield : ' )] + [ '{0:6.1f}%'.format(PLQY_array[ii]*100) for ii in range(data_size) ] ) )
    print( '{0:>15s} {1:>6.1f}% {2:>15s} {3:>6.1f}% '.format( 'Ave. : ', np.mean(PLQY_array)*100, 'Std. : ', np.std(PLQY_array)*100) )
def saveSummary(filepath, fname, A_array, PLQY_array):
    A_array, PLQY_array = np.array(A_array), np.array(PLQY_array)
    data_size = A_array.size

    if not os.path.isdir(filepath):
        os.makedirs(filepath)
    file = open( os.path.join(filepath, fname) ,'w')
    file.write('========================== Summary =========================\n')
    file.write( ' '.join( ['{0:>15s}'.format( 'Absorption : ' )] + [ '{0:6.1f}%'.format(A_array[ii]*100) for ii in range(data_size) ] ) + '\n')
    file.write( '{0:>15s} {1:>6.1f}% {2:>15s} {3:>6.1f}% '.format( 'Ave. : ', np.mean(A_array)*100, 'Std. : ', np.std(A_array)*100) + '\n' )
    file.write( ' '.join( ['{0:>15s}'.format( 'Quantum Yield : ' )] + [ '{0:6.1f}%'.format(PLQY_array[ii]*100) for ii in range(data_size) ] ) + '\n' )
    file.write( '{0:>15s} {1:>6.1f}% {2:>15s} {3:>6.1f}% '.format( 'Ave. : ', np.mean(PLQY_array)*100, 'Std. : ', np.std(PLQY_array)*100) + '\n' )
    file.close()
if __name__ == '__main__':
    # input
    data_size = 5

    # calculate
    CF_pd = read_CFfile( filepath='./data', filename='CF.txt' )
    A_array, PLQY_array = np.zeros( (data_size,), dtype=np.float ), np.zeros( (data_size,), dtype=np.float )
    for ii in range(data_size):
        A_array[ii], PLQY_array[ii] = PLQY_calculator( filepath='./data/PLQY/{0}'.format(ii+1), CF_pd=CF_pd)

    # print information
    printSummary(A_array, PLQY_array)
    saveSummary(filepath='./data/PLQY', fname='summary.txt', A_array=A_array, PLQY_array=PLQY_array)















