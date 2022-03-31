# -*- coding: utf-8 -*-
"""
Created on Jan 21st 2021
Last Update : March 31th, 2022

@author: Alvin Bayudanto
"""

### import libaries
import os
import pandas as pd
import sqlite3
import numpy as np

### Purpose of this py script is to 
    #compile : displacement time histories data
    
    #---for all layers, locations, earthquake design levels, and ground motions of interest
    
## Workflow:
#   - Locate all the target DEEPSOIL DB Folders for all locations, Earthquake design levels, and Ground Motion Time Histories
#   - Generate the List of directories based on the designated folders and files
#   - Extract and compile all the displacement time history data from DEEPSOIL Database for all layers of interest, for this case from top to bottom of soil columns 
#   - Create Dataframe for time vs displacement and export to csv file

#--------------------INPUT DATA--------------------#

#SRA Location - Folder Name for Locations of Interest
SRA_LOCATION=['Santa Clara']
# SRA_LOCATION=['East Portal','Fault Crossing','DTSJ','Diridon','28th St_LP','Santa Clara','NYMF']

#Earthquake Level - List all Earthquake Design Level Folders
EQ_LEVEL=['MCEr ESA','MCEr - Liq']
# EQ_LEVEL=['DBE','MCE','MCEr','MCEr ESA','MCEr - Liq']

#Explanation:
# MCEr - Liq stands for MCER total stress based site response analysis with liquefaction interpretation from CLiq and residual strength
# MCEr ESA stands for MCER effective stress based site response analysis towith excess pore water pressure generation to estimate strength reduction

#Ground Motion Name - List all Ground Motions, Complete Names
GM_LIBRARY=['Motion_Zone1_MCAH_GM01_FP_Scaled','Motion_Zone1_MCAH_GM05_FP_Scaled','Motion_Zone1_MCAH_GM07_FP_Scaled']
# GM_LIBRARY=['Motion_Zone2_975_GM11_FN','Motion_Zone2_975_GM11_FP','Motion_Zone1_MCAH_GM02_FP_Scaled','Motion_Zone1_MCAH_GM08_FN_Scaled','Motion_Zone1_MCAH_GM10_FN_Scaled','Motion_Zone1_MCAH_GM01_FP_Scaled','Motion_Zone1_MCAH_GM05_FP_Scaled','Motion_Zone1_MCAH_GM07_FP_Scaled']

for SRA_LOC in SRA_LOCATION:
    for EQ in EQ_LEVEL:
        for GM in GM_LIBRARY:

            #Read SQL database from DEEPSOIL outputs
            main_directory = r'C:\Users\BAY92591\OneDrive - Mott MacDonald\Desktop\Mott MacDonald\Script Library\python\Geoseismic\Disp TH'
            directory = main_directory+'\\'+SRA_LOC+'\\'+EQ
            
            #Variable Library
            disp=[]
            mid_depth=[]
            strain=[]
            time=[]
            Layer=[]
            
            #Target Layer - List all layers from the top to bottom of soil columns based on location
            if SRA_LOC =='Santa Clara':
                top_lyr=1
                bot_lyr=45
            elif SRA_LOC =='NYMF':
                top_lyr=1
                bot_lyr=53
            elif SRA_LOC =='DTSJ':
                top_lyr=1
                bot_lyr=56
            elif SRA_LOC =='Diridon':
                top_lyr=1
                bot_lyr=52
            elif SRA_LOC =='28th St_LP':
                top_lyr=1
                bot_lyr=57
            elif SRA_LOC =='East Portal':
                top_lyr=1
                bot_lyr=36
            elif SRA_LOC =='Fault Crossing':
                top_lyr=1
                bot_lyr=48
            else:
                Layer=[]
                
            #list all layers into array
            for l in range(top_lyr,bot_lyr+1):
                Layer.append(str(l))
            
            #--------------------PROCESS DATA--------------------#
            
            for LayerNo in Layer:
            
                #Motion Database
                con = sqlite3.connect(os.path.join(directory, GM, 'deepsoilout.db3'))
                cur=con.cursor()
                
                #Extract depth data
                mid_depth1=[]
                for row in cur.execute('SELECT DEPTH_LAYER_MID FROM PROFILES'):
                    mid_depth1.append(row)
                mid_depth.extend([mid_depth1])
                
                #Extract displacement at all depths
                disp1=[]
                for row in cur.execute('SELECT LAYER'+LayerNo+'_DISP FROM TIME_HISTORIES'):
                    disp1.append(row)
                disp.extend([disp1])
                
                #Extract time at all depths
                time1=[]
                for row in cur.execute('SELECT TIME FROM TIME_HISTORIES'):
                    time1.append(row)
                time.extend([time1])
                timeStep = time1[1][0]-time1[0][0]
                con.close()
            
            #Database Creation
            columns=[]
            depth_col=[]
            depth_data_col=[]
            data_col=[]
            dataset=[]
            for i in range(len(Layer)):
                time_column='Time'
                disp_column='Disp_'+Layer[i]+'_ft'
                depth_col.append('Depth_'+Layer[i])
                depth_col.append('Depth_'+Layer[i])
                depth_data_col.extend([0])
                depth_data_col.extend([mid_depth1[i][0]])
                data_col.append(time_column)
                data_col.append(disp_column)
                dataset.extend([time[0:][i]])
                dataset.extend([disp[0:][i]])
            columns.append(depth_col)
            columns.append(depth_data_col)
            columns.append(data_col)
            
            #--------------------OUTPUT DATA--------------------#
            
            #DataFrame and Export to CSV
            df_disp=pd.DataFrame(np.column_stack(dataset),columns=columns)
            disp_df_dir=directory+'\\'+GM+'\disp_library.csv'
            
            df_disp.to_csv(disp_df_dir)

