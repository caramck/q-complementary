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
            print("jobs:"+str(jobs))
            sec_anchors.append(cur_line)
    s.close()


    #Total lines in output file
    sec_anchors.append(len(all_lines))
    print(sec_anchors)

    cur_line=1
    #Pull out SCF and HOMO energies for each calculation of interest
    for i in range(jobs):
        print("i:"+str(i))
        #Look selectively in the range in file corresponding to that calculation
    
        #initiate homoArray outside of loop
        homoArray=[]

        for j in range(sec_anchors[i],sec_anchors[i+1]):
            cur_line+=1
            #search for SCF energy for that calculation
            if all_lines[j].find("$molecule") != -1:
                print("found")
                charge=str(all_lines[j+1])
                print("charge:"+charge)

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
            print("here")
            job_type=0
            neutral_scf=SCF_energy
            neutral_homo=HOMO_energy
        elif "-1 2" in str(charge):
            print("here2")
            job_type=1
            anion_scf=SCF_energy
            anion_homo=HOMO_energy
        elif "1 2" in str(charge):
            print("here3")
            job_type=2
            cation_scf=SCF_energy

    s.close()
    return resultsAr

#read in all files in directory that have specified string in the name 
#e.g. "_dft_" to read in all the files with _dft_ in the name
file_string=sys.argv[1]

#names of columns in excel sheet
df_array=[['File','SCF Neutral (Ha)','SCF Anion (Ha)','SCF Cation (Ha)','HOMO Neutral (Ha)','HOMO Anion (Ha)']]

#search all files in folder for this string, if found, include full file name in array
roots, dirs, files = os.walk(".")
for file_name in files:
    if file_string in file_name:
        results=parse_file(x)
        results.insert(0,file_name)
        df_array.append(results)

#create data frame
df=pd.DataFrame(data=df_array)

print(df)

#further data manipulation

#create excel document
df.to_excel(file_string+".xlsx")



    