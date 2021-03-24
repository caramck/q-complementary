######################
# Name: read_dft_excel.py
# Purpose: 
# Author: Caroline Anne McKeon, Feb 2020, Jan 2021
######################a

import os
import sys
import pandas as pd


def parse_file(file_name):

    #Load output file
    p=open(file_name,"r")
    all_lines=p.readlines()
    p.close()
    #SCF value array
    SCFe=[]
    #HOMO value array
    HOMOe=[]
    
    s=open(file_name,"r")
    
    # This iterating process could be more efficient - put more thought into this.
    # Create anchors for each section
    # Parse output file by job section: job 2 is neutral, job 3 is cation, job 4 is anion
    sec_anchors=[]
    cur_line=1
    #running job tally
    jobs=0

    for line in s:
        #keep counter
        cur_line+=1
        #parse output file for job sections for all three jobs of interest
        if line.find("Running Job") !=-1:
            jobs+=1
            sec_anchors.append(cur_line)
    s.close()


    #Total lines in output file
    sec_anchors.append(len(all_lines))

    cur_line=1
    #Pull out SCF and HOMO energies for each calculation of interest
    for i in range(jobs):
        #Look selectively in the range in file corresponding to that calculation
    
        #initiate homoArray outside of loop
        homoArray=[]

        for j in range(sec_anchors[i],sec_anchors[i+1]):
            cur_line+=1
            #search for SCF energy for that calculation
            if all_lines[j].find("$molecule") != -1:
                charge=str(all_lines[j+1])

            if all_lines[j].find("Total energy in the final basis set") != -1:
                scf_line=str(all_lines[j])
                split=scf_line.split()
                SCF_energy=(float(split[-1]))
           
            # search for HOMO energy for that calculation
        
            if all_lines[j].find("-- Virtual --") != -1:
                HOMOline=str(all_lines[j-1])
                splitB=HOMOline.split()
                homoArray.append(float(splitB[-1]))



        # Compare the saved HOMO energies, pick the highest if there are 2.
        if len(homoArray)==2:
            if homoArray[0]>homoArray[1]:
                HOMO_energy=(homoArray[0])
            else:
                HOMO_energy=(homoArray[1])
        else:
            HOMO_energy=(homoArray[0]) 
     
        
        if "0 1" in str(charge):
            job_type=0
            neutral_scf=SCF_energy
            neutral_homo=HOMO_energy
        elif "-1 2" in str(charge):
            job_type=1
            anion_scf=SCF_energy
            anion_homo=HOMO_energy
        elif "1 2" in str(charge):
            job_type=2
            cation_scf=SCF_energy

    s.close()

    #add results to array
    results_arr=[file_name,neutral_scf,anion_scf,cation_scf,neutral_homo,anion_homo]

    return results_arr

#read in all files in directory that have specified string in the name 
#e.g. "_dft_" to read in all the files with _dft_ in the name
file_string=sys.argv[1]

#names of columns in excel sheet
df_array=[['file','scf_neutral_ha','scf_anion_ha','scf_cation_ha','homo_neutral_ha','homo_anion_ha']]

#search all files in folder for this string, if found, include full file name in array
for roots, dirs, files in os.walk("."):
    for file_name in files:
        if file_string in file_name:
            results=parse_file(file_name)
            df_array.append(results)

#create data frame
df=pd.DataFrame(data=df_array)
df.rename(columns=df.iloc[0])

print(df)

#further data manipulation: TODO
#convert energies of everything to eVs
#for i in range(1,len(df_array[0])):
    #data = df[df_array[0][i]]

#create excel document
df.to_excel(file_string+".xlsx")



    