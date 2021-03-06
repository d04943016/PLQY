# PLQY
Method to calculate the photoluminescence quantum yield (PLQY) proposed by professor Richard H.Friend


Ref. https://onlinelibrary.wiley.com/doi/10.1002/adma.19970090308 

The core code is in PLQY.py. The calculation is based on the numpy and scipy, so please install numpy and scipy.

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
for PyQt5 GUI,

    streamlit run FUI_streamlit.py
for streamlit GUI.

### Calibration File
CF.txt in ./data is the callibration file for the instrument. (real intensity = measured intensity X calibration factor)
The first column is wavelength and the second column is the collibration factors.

There should be two columns in the measured data as shown in ./data/PLQY/1~6. 
Similarly, the first column is wavelength and the second column is the collibration factors.

### GUI
When using the GUI, don't forget to see the information on the terminal.

Preview of GUI built on tkinter:

    python GUI_tkinter.py
    
<p align="center">
<img src="https://github.com/d04943016/PLQY/blob/main/figure/tkinter.png" width="400">
</p>

Preview of GUI built on PyQt5:

    python GUI_PyQt5_main.py

<p align="center">
<img src="https://github.com/d04943016/PLQY/blob/main/figure/PyQt5.png" width="400">
</p>

Preview of GUI built on streamlit:

    streamlit run GUI_streamlit.py

<p align="center">
<img src="https://github.com/d04943016/PLQY/blob/main/figure/streamlit.png" width="500">
</p>

More details are in the usage.pdf.
