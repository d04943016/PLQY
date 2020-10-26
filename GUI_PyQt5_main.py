#!/usr/bin/env python3
# Copyright (c) 2020 Wei-Kai Lee. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-
import sys, os
import numpy as np 
import PLQY

from PyQt5 import QtWidgets, QtGui, QtCore
from GUI_PyQt5 import Ui_MainWindow
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('PLQY calculator')

        # Load Button
        self.ui.pushButton.clicked.connect(self.loadbutton_Clicked)

        # Print File Directory Button
        self.ui.pushButton_2.clicked.connect(self.printfiledirectory_buttonClicked)

        # Calculate Button
        self.ui.pushButton_3.clicked.connect(self.calculate_buttonClicked)

        # Save Button
        self.ui.pushButton_4.clicked.connect(self.save_buttonClicked)

        # data initialize
        self.PathList = None
        self.A_array = None
        self.PLQY_array = None
    # help functions
    def IsInteger(self,strr):
        try:
            datasize = int(strr)
            if datasize<1:
                return False
            return True
        except:
            return False
    def IsFloat(self,strr):
        try:
            datasize = float(strr)
            return True
        except:
            return False
    # clicked function
    def loadbutton_Clicked(self):
        print('Now loading/checking file directory(s)')

        # check data size
        datasize_str = str( self.ui.textBrowser.toPlainText() )
        if self.IsInteger(datasize_str):
            datasize = int(datasize_str)
        else:
            print('Data size shoule be a positive integer.')
            print('Please insert data size again.\n')
            return 

        # Ask the user to select a folder.
        tempt_dir = os.getcwd()
        tempt_dir_list = [None] * datasize
        for ii in range(datasize):
            print("Please select a folder for data {0}".format(ii+1))
            initialdir = QtWidgets.QFileDialog.getExistingDirectory(self, "Please select a folder for data {0}".format(ii+1), tempt_dir )

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
        self.PathList = [None]*datasize 
        for ii in range(datasize):
            self.PathList[ii] = tempt_dir_list[ii]
            print('Directory for data set {0} : {1}'.format(ii+1, self.PathList[ii]) )
        print('\n')
    def printfiledirectory_buttonClicked(self):
        print('Now printing file information...')
        if self.PathList is None:
            print('Directory(s) is empty.\n')
            return 
        for ii in range( len(self.PathList) ):
            print('Directory for data set {0} : {1}'.format(ii+1, self.PathList[ii]) )
        print('\n')
    def calculate_buttonClicked(self):
        print('Now calculating the absorption and the PLQY.')

        # check file path
        if (self.PathList is None) or (len(self.PathList)==0):
            print('Please specify the data directory(s) first.\n')
            return 

        # check execitation wavelength
        ex_Lower_Bnd_str = str( self.ui.textBrowser_2.toPlainText() )
        em_Lower_Bnd_str = str( self.ui.textBrowser_3.toPlainText() )
        ex_Upper_Bnd_str = str( self.ui.textBrowser_4.toPlainText() )
        em_Upper_Bnd_str = str( self.ui.textBrowser_5.toPlainText() )
        if ( self.IsFloat(ex_Lower_Bnd_str) & self.IsFloat(em_Lower_Bnd_str) & self.IsFloat(ex_Upper_Bnd_str) & self.IsFloat(em_Upper_Bnd_str)):
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
        CF_pd = PLQY.read_CFfile( filepath='./data', filename='CF.txt' )
        self.A_array, self.PLQY_array = np.zeros( (len(self.PathList),), dtype=np.float ), np.zeros( (len(self.PathList),), dtype=np.float )
        for ii in range(len(self.PathList)):
            self.A_array[ii], self.PLQY_array[ii] = PLQY.PLQY_calculator( filepath=self.PathList[ii], CF_pd=CF_pd, exciting_range=exciting_range, emission_range=emission_range)

        # print information
        PLQY.printSummary(self.A_array, self.PLQY_array)
        print('\n')
    def save_buttonClicked(self):
        print('Now saving the data')
        if (self.A_array is None) or (self.PLQY_array is None):
            print('Please calculate the data first.')
            return 
        filename, filetype = QtWidgets.QFileDialog.getSaveFileName(
                                      self, caption="Select file", directory=os.getcwd(), filter="text files (*.txt);;all files (*.*)" )
        if len(filename) == 0:
            print('Quit saving the data.\n')
            return 
        fpath, fname = os.path.split(filename)
        PLQY.saveSummary(fpath, fname, self.A_array, self.PLQY_array)
        print('Now successfully save the data.\n')
if __name__ == '__main__':
     app = QtWidgets.QApplication([])
     window = MainWindow()
     window.show()
     sys.exit(app.exec_())












