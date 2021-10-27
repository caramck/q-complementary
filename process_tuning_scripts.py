#%%
#generate_tuning_scripts.py
#Purpose: In a directory, generate some given number of scripts optimizing a range of gamma from a given seed value with given coordinates
import os,sys
import subprocess
import shutil
import wheel
import numpy as np
import xlrd
import openpyxl
import matplotlib as plt
import seaborn as sns
import numpy as np   
import pandas as pd

##########################################################
# Define which functionality this code will use          #
##########################################################

flag=sys.argv[1]

##########################################################
# generate directory of output files                      #
##########################################################
def generate_directory(cwd):
    """
    generate_directory

    :param cwd: current working directory
    :return none
    """
    #make a new directory
    names=cwd.split("/")
    new_dir=str(names[-1])+"_out"
    os.mkdir(new_dir)

    #copy all files with ".out" into this directory
    file_string=".out"
    for roots, dirs, files in os.walk(cwd):
        for file_name in files:
            if file_string in file_name:
                os.system('cp '+file_name+' '+str(new_dir))

##########################################################
# Define file_parser object                              #
##########################################################

#constructor
class file_parser:
    """
   One instance of file parser parses all .out files in a directory.

    """

    #Constructor
    def __init__(self,dir_name):
        """
        file_parser constructor 

        :param self
        :param file_name: string. file to parse
        :return none
        """

        #static attributes
        self.dir_name=dir_name


    def search_all_files(self):
        """
        search_all_files: searches all files and saves output

        :return none
        """

        #TODO edit this and make it into a clean function
        def parse_file(file_name):

            """
            parse_file: searches through a particle file for values of interest and saves

            :return none
            """
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

                    #pull the corresponding gamma for this calculation
                    if all_lines[j].find("omega") != -1:
                        gamma_line=str(all_lines[j])
                        split=gamma_line.split()
                        gamma=(float(split[-1]))
    



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
            results_arr=[file_name,gamma,neutral_scf,anion_scf,cation_scf,neutral_homo,anion_homo]

            return results_arr

        def calc_homo_ip(homo,cation_scf,neutral_scf):
            """
            calc_homo_ip: find difference between given homo and ip values

            :return none
            """
            ip=cation_scf-neutral_scf
            homo_ip=np.absolute(homo+ip)

            return homo_ip
        
        def calc_lumo_ea(lumo,neutral_scf,anion_scf):
            """
            calc_lumo_ea: find difference between given lumo and ea values

            :return none
            """
            ea=neutral_scf-anion_scf
            lumo_ea=np.absolute(lumo+ea)

            return lumo_ea


        #create dataframe headers
        df_array=[['file','gamma','scf_neutral_ha','scf_anion_ha','scf_cation_ha','homo_neutral_ha','homo_anion_ha']]

        #set file extension
        file_string=".out"

        #search all files in folder for this string, if found, include full file name in array
        for roots, dirs, files in os.walk(self.dir_name):
            for file_name in files:
                if file_string in file_name:
                    print("Parsing "+str(file_name))
                    results=parse_file(self.dir_name+"/"+file_name)
                    df_array.append(results)

        #create dataframe
        df=pd.DataFrame(data=df_array)
        df.rename(columns=df.iloc[0])
        df.columns=df.iloc[0]
        
        #add homo +ip and lumo+ea columns to df
        #df["homo_ip"] = ((df["homo_neutral_ha"])+(df["scf_cation_ha"]-df["scf_neutral_ha"]))
        #df["homo_ip"] = (calc_homo_ip(df["homo_neutral_ha"],df["scf_cation_ha"],df["scf_neutral_ha"]))

        #print dataframe
        print(df)

        print(cwd+"/tuning.xlsx")
        #create excel document
        df.to_excel(cwd+"/tuning.xlsx")              

        #create plot and save it
        #sns.lineplot(data=df, x="gamma", y="passengers")

##########################################################
# Parse files in directory                               #
##########################################################

#find current working directory
cwd=os.getcwd()

if flag=="a":
    #create file parser object
    parser=file_parser(cwd)

    #parse files in directory
    parser.search_all_files()

if flag=="b":
    generate_directory(cwd)




# %%
