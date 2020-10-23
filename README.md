# PLQY
Method to calculate the photoluminescence quantum yield (PLQY) proposed by professor Richard H.Friend


Ref. https://onlinelibrary.wiley.com/doi/10.1002/adma.19970090308 

The core code is in PLQY.py and the calculation is based on the numpy and scipy.

    pip install numpy scipy

Besides, there are three different types of graphic user interface (GUI) including tkinter, PyQt5, and streamlit 
so if you would like to use the GUI, please install PyQt5 or streamlit, first. 

    pip install pyqt5
or
    
    pip install streamlit

and execute the module by

    python GUI_tkinter.py
for tkinter GUI

or

    python GUI_PyQt5_main.py
for PyQt5 GUI

or

    streamlit run FUI_streamlit.py
for streamlit GUI.


CF.txt in ./data is the callibration file for the instrument. 
The first column is wavelength and the second column is the collibration factors.

There should be two columns in the measured data as shown in ./data/PLQY/1~6. 
Similarly, the first column is wavelength and the second column is the collibration factors.


