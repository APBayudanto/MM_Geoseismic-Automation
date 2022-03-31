# -*- coding: utf-8 -*-
"""
Created on September 17th, 2021
Last Update : March 31th, 2022

@author: Alvin Bayudanto
"""

### import libaries
import os
import pandas as pd
import sqlite3
import numpy as np

### Purpose of this py script is to
    #Automatically delete target files in listed folders

## Workflow:
#   - Locate all the target DEEPSOIL DB Folders for all Earthquake design levels, location, and Ground Motion Time Histories
#   - Generate the List of directories based on the designated folders
#   - Automatically remove target files in listed folders - Do not forget to Select/Activate the command line by removing the # sign
    
#-------------------- Input Data : Locate all target folder locations--------------------#

#SRA Location
SRA_LOCATION=['DTSJ','Diridon','28th St_LP']
# SRA_LOCATION=['DTSJ','Diridon','28th St_LP']

#Zone Number for Corresponding Locations
for SRALOC in SRA_LOCATION:
    if SRALOC == 'DTSJ':
        Zone_No='2'
    elif SRALOC == 'Diridon':
        Zone_No='1'
    else:
        Zone_No='3'
    
#Earthquake Level
    EQ_LEVEL=['DBE','MCE','MCEr']
    # EQ_LEVEL=['DBE','MCE','MCEr']

#Earthquake Level - Years
    for EQ in EQ_LEVEL:
        if EQ == 'DBE':
            EQ_Year='225'
        elif EQ == 'MCE':
            EQ_Year='975'
        else:
            EQ_Year='MCAH'

#Ground Motion Library
        if SRALOC == 'Diridon':
            GM_TYPE=['FN/FP']
        else:
            GM_TYPE=['H1/H2']
        # GM_TYPE=['H1/H2','FN/FP','LONG/TRANS']
        
        for GMT in GM_TYPE:
            if EQ == 'MCEr':
                if GMT == 'H1/H2':
                    GM_LIST=['GM01_H1_SCALED','GM01_H2_SCALED','GM02_H1_SCALED','GM02_H2_SCALED','GM03_H1_SCALED','GM03_H2_SCALED',
                              'GM04_H1_SCALED','GM04_H2_SCALED','GM05_H1_SCALED','GM05_H2_SCALED','GM06_H1_SCALED','GM06_H2_SCALED',
                              'GM07_H1_SCALED','GM07_H2_SCALED','GM08_H1_SCALED','GM08_H2_SCALED','GM09_H1_SCALED','GM09_H2_SCALED',
                              'GM10_H1_SCALED','GM10_H2_SCALED','GM11_H1_SCALED','GM11_H2_SCALED']
                elif GMT == 'FN/FP':
                    GM_LIST=['GM01_FN_SCALED','GM01_FP_SCALED','GM02_FN_SCALED','GM02_FP_SCALED','GM03_FN_SCALED','GM03_FP_SCALED',
                              'GM04_FN_SCALED','GM04_FP_SCALED','GM05_FN_SCALED','GM05_FP_SCALED','GM06_FN_SCALED','GM06_FP_SCALED',
                              'GM07_FN_SCALED','GM07_FP_SCALED','GM08_FN_SCALED','GM08_FP_SCALED','GM09_FN_SCALED','GM09_FP_SCALED',
                              'GM10_FN_SCALED','GM10_FP_SCALED','GM11_FN_SCALED','GM11_FP_SCALED']
                else:
                    GM_LIST=['GM01_LONG_SCALED','GM01_TRANS_SCALED','GM02_LONG_SCALED','GM02_TRANS_SCALED','GM03_LONG_SCALED','GM03_FP_SCALED',
                              'GM04_LONG_SCALED','GM04_TRANS_SCALED','GM05_LONG_SCALED','GM05_TRANS_SCALED','GM06_LONG_SCALED','GM06_FP_SCALED',
                              'GM07_LONG_SCALED','GM07_TRANS_SCALED','GM08_LONG_SCALED','GM08_TRANS_SCALED','GM09_LONG_SCALED','GM09_FP_SCALED',
                              'GM10_LONG_SCALED','GM10_TRANS_SCALED','GM11_LONG_SCALED','GM11_TRANS_SCALED']
            else:
                if GMT == 'H1/H2':
                    GM_LIST=['GM01_H1','GM01_H2','GM02_H1','GM02_H2','GM03_H1','GM03_H2',
                              'GM04_H1','GM04_H2','GM05_H1','GM05_H2','GM06_H1','GM06_H2',
                              'GM07_H1','GM07_H2','GM08_H1','GM08_H2','GM09_H1','GM09_H2',
                              'GM10_H1','GM10_H2','GM11_H1','GM11_H2']
                elif GMT == 'FN/FP':
                    GM_LIST=['GM01_FN','GM01_FP','GM02_FN','GM02_FP','GM03_FN','GM03_FP',
                              'GM04_FN','GM04_FP','GM05_FN','GM05_FP','GM06_FN','GM06_FP',
                              'GM07_FN','GM07_FP','GM08_FN','GM08_FP','GM09_FN','GM09_FP',
                              'GM10_FN','GM10_FP','GM11_FN','GM11_FP']
                else:
                    GM_LIST=['GM01_LONG','GM01_TRANS','GM02_LONG','GM02_TRANS','GM03_LONG','GM03_FP',
                              'GM04_LONG','GM04_TRANS','GM05_LONG','GM05_TRANS','GM06_LONG','GM06_FP',
                              'GM07_LONG','GM07_TRANS','GM08_LONG','GM08_TRANS','GM09_LONG','GM09_FP',
                              'GM10_LONG','GM10_TRANS','GM11_LONG','GM11_TRANS']
        
            GM_LIBRARY=[]
            for GML in GM_LIST:
                GM_LIBRARY.append('Motion_Zone'+Zone_No+'_'+EQ_Year+'_'+GML)

#Directory and Variable of Interest
            for GM in GM_LIBRARY:

                #Read SQL database from DEEPSOIL outputs
                main_directory = r'C:\Users\BAY92591\OneDrive - Mott MacDonald\Desktop\Mott MacDonald\Script Library\python\Geoseismic\Acc TH'
                directory = main_directory+'\\'+SRALOC+'\\'+EQ

#--------------------PROCESS / List the Target Files which need to be deleted, remove the "#" sign--------------------#
                
                # os.remove(directory+'\\'+GM+'\\deepsoilout.db3')
                # os.remove(directory+'\\'+GM+'\\deepsoilin.txt')
                # os.remove(directory+'\\'+GM+'\\strain.txt')
                # os.remove(directory+'\\'+GM+'\\accTH_library.csv')