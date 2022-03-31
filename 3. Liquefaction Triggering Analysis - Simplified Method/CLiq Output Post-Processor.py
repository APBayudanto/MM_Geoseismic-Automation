# -*- coding: utf-8 -*-
"""
Created on November 11th, 2021
Last Update : March 31th, 2022

@author: Alvin Bayudanto
"""

### import libaries
import xlrd
import copy
import openpyxl
from openpyxl import Workbook
import numpy as np
import os.path
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec
from matplotlib.ticker import MaxNLocator
import pandas as pd
from pandas import DataFrame
from scipy import stats
import statsmodels.api as sm
import pylab as py
from scipy.stats import norm
import matplotlib.mlab as mlab
import statsmodels.api as sm
import statistics
import scipy
from math import log
import matplotlib as mpl

### Purpose of this py script is to
    #Compile and list the location and thickness of liquefied layers from CLiq output with : FS<1 and thickness greater than 0.95 ft criteria
    
    #--- for one location with all earthquake design levels

## Workflow:    
#   - Read/Import CLiq output results (specific to CPTs) in Xlsx files from each earthquake design level folder
#   - List all CPT names of interest, and read corresponding Depth and FS values below 1
#   - Compute and compile new interpreted liquefied layer thickness and depth based on "thickness greater than 0.95 ft" criterion 
#   - Final Dataframes creation for: 1) summary table for all CPTs and 2) interpretation/calculation presented per each CPT
#   - Export to Xlsx files: 1) Master summary table and 2) Result Interpretations for each CPT stored in each tab

#--------------------INPUT DATA--------------------#

#Input your earthquake design level information, stored in different folders
DE_Input_Library=['DBE','MCE','PGAm'] 
# DE_Input_Library=['DBE','MCE','PGAm']

#Input yout list of CPTs
CPT_Data_Library=  ['CPT-090','CPT-091','CPT-092','CPT-093','CPT-157','CPT-173','CPT-173A','CPT-173B',
                    'CPT-174','CPT-174A','CPT-175','CPT-176B','CPT-177','CPT-178','Y&S CPT-001','Y&S CPT-002',
                    'Y&S CPT-003','Y&S CPT-004','Y&S CPT-005','Y&S CPT-006','Y&S CPT-007','Y&S CPT-008','Y&S CPT-009','Y&S CPT-010',
                    'Y&S CPT-011','Y&S CPT-012','Y&S CPT-013','Y&S CPT-014','Y&S CPT-015','Y&S CPT-016','Y&S CPT-017','Y&S CPT-018',
                    'Y&S CPT-019','Y&S CPT-020','Y&S CPT-021','Y&S CPT-022','Y&S CPT-023','Y&S CPT-024','Y&S CPT-025','Y&S CPT-026',
                    'Y&S CPT-027','Y&S CPT-028','Y&S CPT-029','Y&S CPT-030','Y&S CPT-031','Y&S CPT-032','Y&S CPT-033','Y&S CPT-034',
                    'Y&S CPT-035','CPT-189','CPT-190','CPT-192','CPT-194','SCPT-188','SCPT-191','SCPT-193']

#Input your file name
File_name_extension="CLiq Results.xlsx"

for DEI in DE_Input_Library:
    
#--------------------DIRECTORY---------------------#

    calc_dir=r'C:\Users\BAY92591\OneDrive - Mott MacDonald\Desktop\Mott MacDonald\Script Library\python\Geoseismic\CLiq Output'+'\\'
    DE_Input_dir=calc_dir+DEI+'\\'
    CLiq_File=DE_Input_dir+DEI+' '+File_name_extension #Automated file name format = earthquake design level, extension - make sure to be consistent
    
    Depth_Liq_DF=[]
    Top_LL_Depth_DF=[]
    Bottom_LL_Depth_DF=[]
    LL_Thickness_DF=[]
    LL_Criteria_DF=[]
    Real_LL_Thickness_DF=[]
    Total_LL_Thickness_DF=[]
    
    # DATA_SUMMARY_MASTER=[]
    CPT_ID_MASTER=[]
    LL_LayerList_MASTER=[]
    Total_LL_Thickness_MASTER=[]
        
    for CPT_Data in CPT_Data_Library:
        CPT_File=pd.read_excel(CLiq_File,CPT_Data+' - Liq. Results',header=None)
        
#--------------------Data Collection--------------------#

        Depth_Library=np.array(CPT_File[2:][1])
        FS_Library=np.array(CPT_File[2:][26])
        FS_RowNum=np.arange(0,len(FS_Library),1)
        Depth_Liq_DB=[]
        FS_Liq_DB=[]
        
        Depth_Liq_Group=[]
        Depth_Liq_Group1=[]
        Depth_Liq_Group2=[]
        FS_Liq_Group=[]
        FS_Liq_Group1=[]
        FS_Liq_Group2=[]
        
        for i in FS_RowNum:
            if FS_Library[i]<=1:
                Depth_Liq_DB.append(Depth_Library[i])
                FS_Liq_DB.append(FS_Library[i])
            else:
                Depth_Liq_DB.append(' ')
                FS_Liq_DB.append(' ')
        
        #Data Grouping for LL Depth and FS
        for i in FS_RowNum:
            if FS_Liq_DB[i] == ' ':
                Depth_Liq_Group1=[]
                Depth_Liq_Group2=[]
                FS_Liq_Group1=[]
                FS_Liq_Group2=[]
            else:
                Depth_Liq_Group1=Depth_Liq_DB[i]
                FS_Liq_Group1=FS_Liq_DB[i]
                Depth_Liq_Group2.append(Depth_Liq_Group1)
                FS_Liq_Group2.append(FS_Liq_Group1)
                if (i+1)>=len(FS_RowNum):
                    if len(FS_Liq_Group2)>=1:
                        Depth_Liq_Group.append(Depth_Liq_Group2)
                        FS_Liq_Group.append(FS_Liq_Group2)
                        continue
                    else:
                        continue
                else:
                    if FS_Liq_DB[i+1] == ' ':
                        Depth_Liq_Group.append(Depth_Liq_Group2)
                        FS_Liq_Group.append(FS_Liq_Group2)
                    else:
                        continue
                
#--------------------Calculation--------------------#
        
        #Top and Bottom LL Depth (ft)
        DLG_GroupNum=np.arange(0,len(Depth_Liq_Group),1)
        Top_LL_Depth=[]
        Bottom_LL_Depth=[]
        LL_Thickness=[]
        Real_LL_Thickness=[]
        LL_Criteria=[]
        
        # Total_LL_Thickness=[]
        for DLG in DLG_GroupNum:
            Top_LL_Depth.append(min(Depth_Liq_Group[DLG]))
            Bottom_LL_Depth.append(max(Depth_Liq_Group[DLG]))
            
        #LL Thickness (ft)
            LL_Thickness.append(round(max(Depth_Liq_Group[DLG])-min(Depth_Liq_Group[DLG]),2))
        
        #Check if LL Thickness greater than 0.95 ft
        for LLT in LL_Thickness:
            if LLT>0.95:
                Real_LL_Thickness.append(LLT) 
            else:
                Real_LL_Thickness.append(' ')
        
        #LL Meeting Criteria
        for i in range(0,len(Real_LL_Thickness)):
            if Real_LL_Thickness[i]==' ':
                LL_Criteria.append(' ')
            else:
                LL_Criteria.append(str(round(Top_LL_Depth[i],1))+' ft - '+str(round(Bottom_LL_Depth[i],1))+' ft')
                
        #Total Thickness of Liquefied Layer (ft)
        Total_LL_Thickness=0
        for i in range(0,len(Real_LL_Thickness)):
            if Real_LL_Thickness[i]==' ':
                continue
            else:
                Total_LL_Thickness=Total_LL_Thickness+Real_LL_Thickness[i]
            
#--------------------Interpretation Database Creation--------------------#            
         
        Top_LL_Depth_LIB=[]
        Bottom_LL_Depth_LIB=[]
        LL_Thickness_LIB=[]
        LL_Criteria_LIB=[]
        Real_LL_Thickness_LIB=[]
        Total_LL_Thickness_LIB=[Total_LL_Thickness]
        
        Top_LL_Depth_LIB.extend(Top_LL_Depth)
        Bottom_LL_Depth_LIB.extend(Bottom_LL_Depth)
        LL_Thickness_LIB.extend(LL_Thickness)
        LL_Criteria_LIB.extend(LL_Criteria)
        Real_LL_Thickness_LIB.extend(Real_LL_Thickness)
        for i in range(0,len(Top_LL_Depth_LIB)-1):
            Total_LL_Thickness_LIB.append(' ')
        
        for i in range(0,len(FS_RowNum)-len(Real_LL_Thickness_LIB)):
            Top_LL_Depth_LIB.append(' ')
            Bottom_LL_Depth_LIB.append(' ')
            LL_Thickness_LIB.append(' ')
            LL_Criteria_LIB.append(' ')
            Real_LL_Thickness_LIB.append(' ')
        for i in range(0,len(FS_RowNum)-len(Total_LL_Thickness_LIB)):
            Total_LL_Thickness_LIB.append(' ')
        
        CPT_ID_MASTER.append(CPT_Data)
        LL_LayerList=[]
        for LLC in LL_Criteria_LIB:
            if LLC == ' ':
                continue
            else:
                LL_LayerList.append(LLC)
        LL_LayerList_MASTER.append(LL_LayerList)
        Total_LL_Thickness_MASTER.append(Total_LL_Thickness)
        
#--------------------Interpretation Export to Spreadsheet--------------------#
        
        Depth_Liq_DF.append(Depth_Liq_DB)
        Top_LL_Depth_DF.append(Top_LL_Depth_LIB)
        Bottom_LL_Depth_DF.append(Bottom_LL_Depth_LIB)
        LL_Thickness_DF.append(LL_Thickness_LIB)
        LL_Criteria_DF.append(LL_Criteria_LIB)
        Real_LL_Thickness_DF.append(Real_LL_Thickness_LIB)
        Total_LL_Thickness_DF.append(Total_LL_Thickness_LIB)
    
    writer = pd.ExcelWriter(calc_dir+DEI+'\\'+DEI+' CLiq Results Interpretation.xlsx', engine='xlsxwriter')
    DATA_SUMMARY_MASTER=[]
    
    for i in range(0,len(Total_LL_Thickness_DF)):
        DATA_SUMMARY=pd.DataFrame({'Depth (ft) for FS > 1': Depth_Liq_DF[i],'LL Top Depth (ft)': Top_LL_Depth_DF[i],'LL Bottom Depth (ft)': Bottom_LL_Depth_DF[i],
                                   'LL Layer Thickness (ft)': LL_Thickness_DF[i],'LL > 0.95 ft?': Real_LL_Thickness_DF[i],'LL Meeting Criteria': LL_Criteria_DF[i],
                                   'Total LL Thickness (ft)': Total_LL_Thickness_DF[i]})
        DATA_SUMMARY_MASTER.append(DATA_SUMMARY)
    
    for i in range(0,len(CPT_Data_Library)):
        DATA_SUMMARY_MASTER[i].to_excel(writer,CPT_Data_Library[i]+ ' Interpretation', index = False)
    
    writer.save()
    writer.close()
    
#--------------------Master Summary Export to Spreadsheet--------------------#
    
    writer = pd.ExcelWriter(calc_dir+DEI+'\\'+DEI+' CLiq Interpretation Master Summary.xlsx', engine='xlsxwriter')
    DATA_SUMMARY=pd.DataFrame({'CPT ID': CPT_ID_MASTER,'List of Liquefied Layers': LL_LayerList_MASTER,'Total Liquefied Layer Thickness (ft)': Total_LL_Thickness_MASTER})
    DATA_SUMMARY.to_excel(writer,'Summary of Interpretation', index = False)
    writer.save()
    writer.close()