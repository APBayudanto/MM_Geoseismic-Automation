# -*- coding: utf-8 -*-
"""
Created on Jan 21st 2021
Last Update : March 31th, 2022

@author: Alvin Bayudanto
"""

### import libraries
import os
import pandas as pd
import sqlite3
import numpy as np

### Purpose of this py script is to 
    #compile : surface response spectra, maximum shear strain profile 
    #compute and summarize : mobilized shear stress profile based on max shear stress ratio and initial effective vertical stress
    
    #---for all locations, earthquake design levels, and ground motions of interest

## Workflow:
#   - Locate all the target DEEPSOIL DB Folders for all locations, Earthquake design levels, and Ground Motion Time Histories
#   - Generate the List of directories based on the designated folders and files
#   - Extract and compile (and compute when necessary) surface response spectra, max shear strain profile, and mobilized shear stress profile
#   - Create Dataframe for Period vs Sa; Depth vs Max Shear Strain; Depth vs Mobilized Shear Stress and export to csv file

#--------------------INPUT DATA--------------------#

#SRA Location
SRA_LOCATION=['Newhall Yard & Maintenance Facility']
# SRA_LOCATION=['Santa Clara Station','Santa Clara Station - Sensitivity Analysis','Newhall Yard & Maintenance Facility']

#Earthquake Level
EQ_LEVEL=['DBE','MCE','MCEr']
# EQ_LEVEL=['DBE','MCE','MCEr','MCEr ESA','MCEr - Liq']

#GM List
GM_LIST=['GM01_FN','GM01_FP','GM02_FN','GM02_FP','GM03_FN','GM03_FP','GM04_FN','GM04_FP',
          'GM05_FN','GM05_FP','GM06_FN','GM06_FP','GM07_FN','GM07_FP','GM08_FN','GM08_FP',
          'GM09_FN','GM09_FP','GM10_FN','GM10_FP','GM11_FN','GM11_FP']
# GM_LIST=['GM01_FN','GM01_FP','GM02_FN','GM02_FP','GM03_FN','GM03_FP','GM04_FN','GM04_FP',
#          'GM05_FN','GM05_FP','GM06_FN','GM06_FP','GM07_FN','GM07_FP','GM08_FN','GM08_FP',
#          'GM09_FN','GM09_FP','GM10_FN','GM10_FP','GM11_FN','GM11_FP']

for SRA_LOC in SRA_LOCATION:
    for EQ in EQ_LEVEL:
        
        #Ground Motion Name
        GM_LIBRARY=[]
        for GML in GM_LIST:
            if SRA_LOC =='Newhall Yard & Maintenance Facility' or 'Santa Clara Station':
                if EQ =='DBE':
                    GM_LIBRARY.append('Motion_Zone1_225_'+GML)
                elif EQ =='MCE':
                    GM_LIBRARY.append('Motion_Zone1_975_'+GML)
                else:
                    GM_LIBRARY.append('Motion_Zone1_MCAH_'+GML+'_Scaled')
        
        #Define the variables
        Period_lib=[]
        Mid_Depth_lib=[]
        Surface_Sa_lib=[]
        Max_Shear_Strain_lib=[]
        Initial_eff_ver_stress_lib=[]
        Max_Stress_Ratio_lib=[]
        Mob_Shear_Stress_lib=[]
        
        for GM in GM_LIBRARY:

            #Read SQL database from DEEPSOIL outputs
            main_directory = r'C:\Users\BAY92591\OneDrive - Mott MacDonald\Desktop\Mott MacDonald\Script Library\python\Geoseismic\SRA post-processing'
            data_directory = main_directory+'\\'+SRA_LOC+'\\'+EQ+'\\'+GM
            output_directory = main_directory+'\\'+SRA_LOC+'\\'+EQ
            
            #Variable Library
            Period=[]
            Mid_Depth=[]
            Surface_Sa=[]
            Max_Shear_Strain=[]
            Initial_eff_ver_stress=[]
            Max_Stress_Ratio=[]
            Mob_Shear_Stress=[]
            
            #--------------------PROCESS DATA--------------------#
            
            #Motion Database
            con = sqlite3.connect(os.path.join(data_directory, 'deepsoilout.db3'))
            cur=con.cursor()
            
            #Extract depth data
            Mid_Depth1=[]
            for row in cur.execute('SELECT DEPTH_LAYER_MID FROM PROFILES'):
                Mid_Depth1.append(row)
            Mid_Depth.extend(Mid_Depth1)
            
            #Extract max shear strain at all depths
            Max_Shear_Strain1=[]
            for row in cur.execute('SELECT MAX_STRAIN FROM PROFILES'):
                Max_Shear_Strain1.append(row)
            Max_Shear_Strain.extend(Max_Shear_Strain1)
            
            #Extract Period data
            Period1=[]
            for row in cur.execute('SELECT PERIOD FROM RESPONSE_SPECTRA'):
                Period1.append(row)
            Period.extend(Period1)
            
            #Extract Surface Response Spectra at ground surface
            Surface_Sa1=[]
            for row in cur.execute('SELECT LAYER1_RS FROM RESPONSE_SPECTRA'):
                Surface_Sa1.append(row)
            Surface_Sa.extend(Surface_Sa1)
            
            ##--Mobilized Shear Stress Profile Computation--##
            
            #Extract Initial eff. vertical stress at all depths
            Initial_eff_ver_stress1=[]
            for row in cur.execute('SELECT INITIAL_EFFECTIVE_STRESS FROM PROFILES'):
                Initial_eff_ver_stress1.append(row)
            Initial_eff_ver_stress.extend(Initial_eff_ver_stress1)
            
            #Extract max stress ratio at all depths
            Max_Stress_Ratio1=[]
            for row in cur.execute('SELECT MAX_STRESS_RATIO FROM PROFILES'):
                Max_Stress_Ratio1.append(row)
            Max_Stress_Ratio.extend(Max_Stress_Ratio1)
            
            #Compute Mob. shear stress at all depths
            for mss in range(len(Max_Stress_Ratio)):
                Mob_Shear_Stress.append(tuple(elem_1*elem_2 for elem_1,elem_2 in zip(Max_Stress_Ratio[mss],Initial_eff_ver_stress[mss])))
            
            #Data Library
            Period_lib.append(Period)
            Mid_Depth_lib.append(Mid_Depth)
            Surface_Sa_lib.append(Surface_Sa)
            Max_Shear_Strain_lib.append(Max_Shear_Strain)
            Initial_eff_ver_stress_lib.append(Initial_eff_ver_stress)
            Max_Stress_Ratio_lib.append(Max_Stress_Ratio)
            Mob_Shear_Stress_lib.append(Mob_Shear_Stress)
            
        #DATABASE CREATION and OUTPUT EXTRACTION & PRODUCTION-----------------------------------------------
        
        ###------------Surface Response Spectra------------###
        
        Columns=[]
        RS_columns=[]
        RS_data_col=[]
        RS_dataset=[]
        RS_dataset.append(Period_lib[0:][0])
        for i in range(len(GM_LIST)):
            Period_column='Period (s)'
            RS_columns='Surface RS_'+EQ+'_'+GM_LIST[i]+' (g)'
            if i==0:
                RS_data_col.append(Period_column)
                RS_data_col.append(RS_columns)
            else:
                RS_data_col.append(RS_columns)
            RS_dataset.append(Surface_Sa_lib[0:][i])
        
        #-OUTPUT DATA-#
        
        #DataFrame and Export to CSV
        df_RS=pd.DataFrame(np.column_stack(RS_dataset),columns=RS_data_col)
        RS_df_dir=output_directory+'\Surface Sa_library.csv'
        df_RS.to_csv(RS_df_dir)
        
        
        ###------------Max Shear Strain Profile------------###
        
        Columns=[]
        MSS_columns=[]
        MSS_data_col=[]
        MSS_dataset=[]
        MSS_dataset.append(Mid_Depth_lib[0:][0])
        for i in range(len(GM_LIST)):
            MidDepth_column='Depth (ft)'
            MSS_columns='Max Shear Strain_'+EQ+'_'+GM_LIST[i]+' (%)'
            if i==0:
                MSS_data_col.append(MidDepth_column)
                MSS_data_col.append(MSS_columns)
            else:
                MSS_data_col.append(MSS_columns)
            MSS_dataset.append(Max_Shear_Strain_lib[0:][i])
        
        #-OUTPUT DATA-#
        
        #DataFrame and Export to CSV
        df_MSS=pd.DataFrame(np.column_stack(MSS_dataset),columns=MSS_data_col)
        MSS_df_dir=output_directory+'\Max Shear Strain Profile_library.csv'
        df_MSS.to_csv(MSS_df_dir)
        
        ###------------Mobilized Shear Stress Profile------------###
        
        Columns=[]
        mobss_columns=[]
        mobss_data_col=[]
        mobss_dataset=[]
        mobss_dataset.append(Mid_Depth_lib[0:][0])
        for i in range(len(GM_LIST)):
            MidDepth_column='Depth (ft)'
            mobss_columns='Mobilized Shear Stress_'+EQ+'_'+GM_LIST[i]+' (psf)'
            if i==0:
                mobss_data_col.append(MidDepth_column)
                mobss_data_col.append(mobss_columns)
            else:
                mobss_data_col.append(mobss_columns)
            mobss_dataset.append(Mob_Shear_Stress_lib[0:][i])
        
        #-OUTPUT DATA-#
        
        #DataFrame and Export to CSV
        df_mobss=pd.DataFrame(np.column_stack(mobss_dataset),columns=mobss_data_col)
        mobss_df_dir=output_directory+'\Mobilized Shear Stress Profile_library.csv'
        df_mobss.to_csv(mobss_df_dir)