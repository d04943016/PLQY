import os
import streamlit as st
import PLQY
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def PlotData(user_input, filelist, Index):
    filelist[Index] = user_input
    for fname in PLQY.measuredFilenameList:
        if not os.path.isfile( os.path.join(user_input, fname) ):
            st.write('File {0} is not in {1}.\n'.format(fname, user_input) )
            filelist[Index] = None
    if (filelist[Index] is not None):
        PdFrameList = [ pd.read_csv( os.path.join(filelist[Index],fname), sep=r"\s+|;|:|\t",header=None, engine='python' ) for fname in PLQY.measuredFilenameList] 
        wvList  = [ data_pd.values[:,0] for data_pd in PdFrameList ]
        intensityList = [data_pd.values[:,1] for data_pd in PdFrameList ]
        fig, ax = plt.subplots(2, 1)
        ax[0].plot(wvList[0], intensityList[0], label='A1')
        ax[0].plot(wvList[1], intensityList[1], label='B1')
        ax[0].plot(wvList[2], intensityList[2], label='C1')
        ax[0].legend()
        ax[1].plot(wvList[3], intensityList[3], label='A2')
        ax[1].plot(wvList[4], intensityList[4], label='B2')
        ax[1].legend()
        st.pyplot(fig) 
def main(CF_pd):
    st.title('PLQY Calculator')
    st.write("This is a calculator to calculate PLQY proposed by prof. Richard H. Friend et. al. ")
    st.write("Ref: https://onlinelibrary.wiley.com/doi/abs/10.1002/adma.19970090308")
    # Measured Data Information
    st.header('Measurement Condition')
    st.write('***A1*** : ***activation*** light wavelength range when there is ***no sample*** in the integrating sphere' )
    st.write('***B1*** : ***activation*** light wavelength range when sample is in the sphere but light ***does not*** hit on the sample')
    st.write('***B2*** : ***emission*** light wavelength range when sample is in the sphere but light ***does not*** hit on the sample')
    st.write('***C1*** : ***activation*** light wavelength range when sample is in the sphere and light hits on the sample')
    st.write('***C2*** : ***emission*** light wavelength range when sample is in the sphere and light hits on the sample')
    st.write('\n\n')

    # Step 1
    data_size = 6
    filelist = [None] * data_size
    A_array, PLQY_array = np.zeros( (data_size,), dtype=np.float ), np.zeros( (data_size,), dtype=np.float )

    st.header('Step 1 : Load Data (Maximum Data Size : {0})'.format(data_size))
    st.write('defualt directory : ', os.getcwd())

    user_input0 = st.text_input("Insert Data Directory", os.getcwd(), key='user_input0')
    PlotData(user_input0, filelist, Index = 0) 

    user_input1 = st.text_input("Insert Data Directory", os.getcwd(), key='user_input1')
    PlotData(user_input1, filelist, Index = 1) 

    user_input2 = st.text_input("Insert Data Directory", os.getcwd(), key='user_input2')
    PlotData(user_input2, filelist, Index = 2) 

    user_input3 = st.text_input("Insert Data Directory", os.getcwd(), key='user_input3')
    PlotData(user_input3, filelist, Index = 3) 

    user_input4 = st.text_input("Insert Data Directory", os.getcwd(), key='user_input4')
    PlotData(user_input4, filelist, Index = 4) 

    user_input5 = st.text_input("Insert Data Directory", os.getcwd(), key='user_input5')
    PlotData(user_input5, filelist, Index = 5) 

    st.write('\n\n')

    # Step 2
    st.header('Step 2 : Excitation Wavelength Range')
    exciting_lower_bnd = st.number_input('Lower Bound', min_value=1, value=315, step=1, format='%d', key='EXECUTION_LOWER_BND_Input')
    exciting_upper_bnd = st.number_input('Upper Bound', min_value=1, value=335, step=1, format='%d', key='EXECUTION_UPPPER_BND_Input')
    st.write('\n\n')

    # Step 3
    st.header('Step 3 : Emisssion Wavelength Range')
    emission_lower_bnd = st.number_input('Lower Bound', min_value=1, value=400, step=1, format='%d', key='EMISSION_LOWER_BND_Input')
    emission_upper_bnd = st.number_input('Upper Bound', min_value=1, value=720, step=1, format='%d', key='EMISSION_UPPPER_BND_Input')
    st.write('\n\n')

    # Step 4
    st.header('Step 4 : Calculate PLQY')
    if st.button('Calculate'):
        PdDataListList = []
        IndexList = []
        exciting_range=(exciting_lower_bnd, exciting_upper_bnd)
        emission_range=(emission_lower_bnd, emission_upper_bnd)

        for ii in range(data_size):
            if (filelist[ii] is not None):
                A_array[ii], PLQY_array[ii] = \
                        PLQY.PLQY_calculator( filepath=filelist[ii], CF_pd=CF_pd, exciting_range=exciting_range, emission_range=emission_range)

                PdFrameList = [ pd.read_csv( os.path.join(filelist[ii],fname), sep=r"\s+|;|:|\t",header=None, engine='python' ) for fname in PLQY.measuredFilenameList] 
                PdDataListList.append(PdFrameList)
                IndexList.append(ii+1)
        A_array_tempt = np.array( [A_array[ii-1] for ii in IndexList])
        PLQY_array_tempt = np.array( [PLQY_array[ii-1] for ii in IndexList])
        # PLQY.printSummary(A_array_tempt, PLQY_array_tempt)

        st.write('Data:')
        st.write( pd.DataFrame( {'Absorption (%)':A_array_tempt*100, 'PLQY (%)':PLQY_array_tempt*100} ))

        st.write('Statistics:')
        st.write( pd.DataFrame( {'Absorption (%)':[np.mean(A_array_tempt)*100, np.std(A_array_tempt)*100], 
                                 'PLQY (%)':[np.mean(PLQY_array_tempt)*100, np.std(PLQY_array_tempt)*100] },
                                 index=['Average', 'Standard Deviation'] ))
        
        st.write('Plot:')
        for jj, name in enumerate(PLQY.measuredFilenameList):
            st.write(name[:-3:], ' : ')
            fig, ax = plt.subplots()
            for ii, PDFrameList in enumerate(PdDataListList):
                data_pd = PDFrameList[jj] 
                wv, intensity = data_pd.values[:,0], data_pd.values[:,1]
                ax.plot(wv, intensity, label='Data number : {0}'.format(IndexList[ii]) )
            ax.legend()
            st.pyplot(fig) 

    st.write('\n\n')

if __name__ == '__main__':
    CF_pd = PLQY.read_CFfile( filepath='./data', filename='CF.txt' )
    main(CF_pd)








