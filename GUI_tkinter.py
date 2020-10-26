#!/usr/bin/env python3
# Copyright (c) 2018 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-

# python module
import sys, os
import os

# third party module
import numpy as np 
import PLQY
import tkinter as tk
from tkinter import filedialog

# windows
window = tk.Tk()
window.title('PLQY calculator')
window.geometry('300x450')

# global variable
global _PathList, _A_array, _PLQY_array
_PathList = None
_A_array = None
_PLQY_array = None

# function
def IsInteger(strr):
    try:
        datasize = int(strr)
        if datasize<1:
            return False
        return True
    except:
        return False
def IsFloat(strr):
    try:
        datasize = float(strr)
        return True
    except:
        return False
# Data Size
datasize_var = tk.StringVar()
datasize_text = tk.Label(window, text='Data Size').place(x=10, y=14)
datasize_entry = tk.Entry(window, textvariable=datasize_var, bd=3 ).place(x=90, y=10)
datasize_var.set('5')

# excitation wavelength
ex_text = tk.Label(window, text='Excitation Wavelength').place(x=10, y=54)

ex_lower_bnd_var = tk.StringVar()
ex_lower_bnd_text = tk.Label(window, text='          Lower Bound').place(x=20, y=84)
ex_lower_bnd_entry = tk.Entry(window, textvariable=ex_lower_bnd_var, bd=3, width=13 ).place(x=150, y=80)
ex_lower_bnd_var.set('315')

ex_upper_bnd_var = tk.StringVar()
ex_upper_bnd_text = tk.Label(window, text='          Upper Bound').place(x=20, y=114)
ex_upper_bnd_entry = tk.Entry(window, textvariable=ex_upper_bnd_var, bd=3, width=13 ).place(x=150, y=110)
ex_upper_bnd_var.set('335')

# emission wavelength
em_text = tk.Label(window, text='Emission Wavelength').place(x=10, y=144)

em_lower_bnd_var = tk.StringVar()
em_lower_bnd_text = tk.Label(window, text='          Lower Bound').place(x=20, y=174)
em_lower_bnd_entry = tk.Entry(window, textvariable=em_lower_bnd_var, bd=3, width=13 ).place(x=150, y=170)
em_lower_bnd_var.set('400')

em_upper_bnd_var = tk.StringVar()
em_upper_bnd_text = tk.Label(window, text='          Upper Bound').place(x=20, y=204)
em_upper_bnd_entry = tk.Entry(window, textvariable=em_upper_bnd_var, bd=3, width=13 ).place(x=150, y=200)
em_upper_bnd_var.set('720')

# 
# Load Data
def load_command_callback():
    print('Now loading/checking file directory(s)')
    if IsInteger(datasize_var.get()):
        datasize = int(datasize_var.get())
    else:
        print('Data size shoule be a positive integer.')
        print('Please insert data size again.\n')
        return 

    # Ask the user to select a folder.
    tempt_dir = os.getcwd()
    tempt_dir_list = [None] * datasize
    for ii in range(datasize):
        print("Please select a folder for data {0}".format(ii+1))
        initialdir = tk.filedialog.askdirectory( title="Please select a folder for data {0}".format(ii+1),
                                                 initialdir=tempt_dir )
        if len(initialdir)==0:
            print('Quit loading the file directory\n')
            return 
        for fname in PLQY.measuredFilenameList:
            if not os.path.isfile( os.path.join(initialdir, fname) ):
                print('File {0} is not in {1}.\n'.format(fname, initialdir) )
                return 
        tempt_dir = os.path.dirname(initialdir)
        tempt_dir_list[ii] = initialdir

    # Insert 
    global _PathList
    _PathList = [tk.StringVar() for ii in range(datasize) ] 
    for ii in range(datasize):
        _PathList[ii].set( tempt_dir_list[ii] )
        print('Directory for data set {0} : {1}'.format(ii+1, _PathList[ii].get()) )
    print('\n')

Load_Button = tk.Button(window,text="Load Data",width=30,height=2, command=load_command_callback).place(x=10, y=240)


# print file path
def print_file_path_callback():
    global _PathList
    print('Now printing file information...')
    if _PathList is None:
        print('Directory(s) is empty.\n')
        return 
    for ii in range( len(_PathList) ):
        print('Directory for data set {0} : {1}'.format(ii+1, _PathList[ii].get()) )
    print('\n')
Print_Filepath_Button = tk.Button(window,text="Print File Path",width=30,height=2, command=print_file_path_callback).place(x=10, y=280)

# calculate result
def calculate_callback():
    print('Now calculating the absorption and the PLQY.')
    # check file path
    global _PathList, _A_array, _PLQY_array
    if (_PathList is None) or (len(_PathList)==0):
        print('Please specify the data directory(s) first.\n')
        return 

    # check execitation wavelength
    ex_Lower_Bnd_str = ex_lower_bnd_var.get()
    em_Lower_Bnd_str = ex_upper_bnd_var.get()
    ex_Upper_Bnd_str = em_lower_bnd_var.get()
    em_Upper_Bnd_str = em_upper_bnd_var.get()
    if ( IsFloat(ex_Lower_Bnd_str) & IsFloat(em_Lower_Bnd_str) & IsFloat(ex_Upper_Bnd_str) & IsFloat(em_Upper_Bnd_str)):
        exciting_lower_bnd = float( ex_Lower_Bnd_str )
        emission_lower_bnd = float( em_Lower_Bnd_str )
        exciting_upper_bnd = float( ex_Upper_Bnd_str )
        emission_upper_bnd = float( em_Upper_Bnd_str )
        if not ((exciting_upper_bnd>exciting_lower_bnd) & (emission_upper_bnd>emission_lower_bnd)):
            print('The upper bound must be larger than the lower bound.\n')
            return 
        if exciting_lower_bnd<250:
            print('The excitation wavelength should be larger than/equal to 250 nm.\n')
            return 
    else:
        print('The excitation wavelength should be a float and larger than/equal to 250 nm.\n')
        return 

    # wavelength range
    exciting_range=(exciting_lower_bnd, exciting_upper_bnd)
    emission_range=(emission_lower_bnd, emission_upper_bnd)
    PLQY.printBound(exciting_range=exciting_range, emission_range=emission_range )

    # calculate the data
    filepath_list = [var.get() for var in _PathList ]
    CF_pd = PLQY.read_CFfile( filepath='./data', filename='CF.txt' )
    _A_array, _PLQY_array = np.zeros( (len(filepath_list),), dtype=np.float ), np.zeros( (len(filepath_list),), dtype=np.float )
    for ii in range(len(filepath_list)):
        _A_array[ii], _PLQY_array[ii] = PLQY.PLQY_calculator( filepath=filepath_list[ii], CF_pd=CF_pd, exciting_range=exciting_range, emission_range=emission_range)
    
    # print information
    PLQY.printSummary(_A_array, _PLQY_array)
    print('\n')
Calculate_Data_Button = tk.Button(window,text="Calculate",width=30,height=2, command=calculate_callback).place(x=10, y=320)

# Save Button
def save_callback():
    print('Now saving the data')
    global _A_array, _PLQY_array
    if (_A_array is None) or (_PLQY_array is None):
        print('Please calculate the data first.')
        return 
    filename = tk.filedialog.asksaveasfilename(initialdir = os.getcwd(),
                                               title = "Select file",
                                               initialfile = 'summary.txt',
                                               filetypes = (("text files","*.txt"),("all files","*.*")))
    if len(filename) == 0:
        print('Quit saving the data.\n')
        return 
    fpath, fname = os.path.split(filename)
    PLQY.saveSummary(fpath, fname, _A_array, _PLQY_array)
    print('Now successfully save the data.\n')

Save_Data_Button = tk.Button(window,text="Save Summary",width=30,height=2, command=save_callback).place(x=10, y=360)

# show
window.mainloop()




