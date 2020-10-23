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
window.geometry('300x400')

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

# execition wavelength
# Data Size
ex_wv_var = tk.StringVar()
ex_wv_text = tk.Label(window, text='Execition Wavelength').place(x=10, y=54)
ex_wv_entry = tk.Entry(window, textvariable=ex_wv_var, bd=3, width=13 ).place(x=150, y=50)
ex_wv_var.set('325')

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
        tempt_dir = initialdir
        tempt_dir_list[ii] = initialdir

    # Insert 
    global _PathList
    _PathList = [tk.StringVar() for ii in range(datasize) ] 
    for ii in range(datasize):
        _PathList[ii].set( tempt_dir_list[ii] )
        print('Directory for data set {0} : {1}'.format(ii+1, _PathList[ii].get()) )
    print('\n')

Load_Button = tk.Button(window,text="Load Data",width=30,height=2, command=load_command_callback).place(x=10, y=140)


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
Print_Filepath_Button = tk.Button(window,text="Print File Path",width=30,height=2, command=print_file_path_callback).place(x=10, y=190)

# calculate result
def calculate_callback():
    print('Now calculating the absorption and the PLQY.')
    # check file path
    global _PathList, _A_array, _PLQY_array
    if (_PathList is None) or (len(_PathList)==0):
        print('Please specify the data directory(s) first.\n')
        return 

    # check execitation wavelength
    if IsFloat(ex_wv_var.get()):
        exciting_center_wv = float( ex_wv_var.get() )
        if exciting_center_wv<250:
            print('The excitation wavelength should be larger than/equal to 250 nm.\n')
            return 
    else:
        print('The excitation wavelength should be a float and larger than/equal to 250 nm.\n')
        return 

    # calculate the data
    filepath_list = [var.get() for var in _PathList ]
    CF_pd = PLQY.read_CFfile( filepath='./data', filename='CF.txt' )
    _A_array, _PLQY_array = np.zeros( (len(filepath_list),), dtype=np.float ), np.zeros( (len(filepath_list),), dtype=np.float )
    for ii in range(len(filepath_list)):
        _A_array[ii], _PLQY_array[ii] = PLQY.PLQY_calculator( filepath=filepath_list[ii], exciting_center_wv=exciting_center_wv, CF_pd=CF_pd)
    # print information
    PLQY.printSummary(_A_array, _PLQY_array)
    print('\n')
Calculate_Data_Button = tk.Button(window,text="Calculate",width=30,height=2, command=calculate_callback).place(x=10, y=240)

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

Save_Data_Button = tk.Button(window,text="Save",width=30,height=2, command=save_callback).place(x=10, y=290)

# show
window.mainloop()




