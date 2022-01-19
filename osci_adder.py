#%%
# Import relevant libraries
from pylab import *
from random import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import os

###MODEL

##Goal: Run in a directory with a series of subdirectories each containing a molecule
##instance: Each directory in directory (each "molecule")

#load samia's excel data sheet into a pandas dataframe

    #Create a new instance of class for each directory (attributes: molecule, tda, )
        #open the directory (self.open_directory())
        #for each file with the label "bse.out"
            #open file
            #parse excitation energies.
            #for each found excitation:
                #check if the excitation energy matches a value in Samia's excel data sheet
                    #check molecule
                    #check TDA status
                    #check xcf-basis
                    #check excitation itself
                    #if rounded singlet value matches parsed value to two decimal places:
                        #add molecule (self.molecule()), tda status (self.tda_status()), excitation and oscillator strength to samia's data structure in new column for that entry)
    
#if there is a directory labelled "tda" in directory, make another instance of the class and repeat with new tda_status

#result: a modified version of Samia's spreadsheet, with oscillator strengths added for the xcf-basis category for all molecules


class osci_adder:

    """
    Class for molecule with a corresponding directory name in an xcf-basis directory.
    """
   
    #Constructor
    def __init__(self, m_name, m_tda, m_method):
        """
        osci_adder class constructor. 

        :param self
        :param molecule_name: str. Could be any of the 28 molecules, name of directory.
        :param tda: int. Either 1 or 0, indicating if it was the data from the tda folder for that molecule instance. 
        :return none
        """

        #Define static attributes
        self.molecule_name = m_name

        self.tda = m_tda  
        
        self.method = m_method

    #Decorator functions for spin array
    #@property
    def molecule_name(self):
        """
        pull molecule name as designated in instance

        :param self
        :return molecule_name
        """
        return self._molecule_name

    #@property
    def tda(self):
        """
        pull tda status as designated in instance
        :param self
        :return tda
        """
        return self._tda

    #@property
    def method(self):
        """
        pull method status as designated in instance
        :param self
        :return method
        """
        return self._method

    def extract_singlets(self,input_path,df_samia):
        """
        Open bse.out file in whatever current directory is.
        Find all singlet energies, oscillator strengths

        This should return an array with: [['molecule','tda','method','energy','osc strength']]
        molecule, tda, and method come from constructor, static attributes.
        energy and osc strength come from file being parsed, variable attributes.

        :param self
        :return extract_singlets_array
        """

        def parse_molgw(input_path,molecule_name,tda,method,df_samia):
            """
            Parse molgw output file
            :param input_path
            :return extract_singlets_array
            """
            #Read in all lines of file to reference later
            m=open(input_path,"r")
            all_lines=m.readlines()
            m.close()

            #dataframe array
            parse_molgw_array=[]
            
            
            #dataframe format: [['a','b','c','d']]
            with open (input_path,"r") as f:
                #create overall dataframe array
                current_line=1

                for line in f:
                    current_line+=1

                    if (line.find(" :       ")) != -1:
                        line_exc=[]
                        line_split=line.split()
                        
                        #add molecule, tda, and method
                        line_exc.append(molecule_name)
                        
                        line_exc.append(tda)
                        
                        line_exc.append(method)
                       
                        
                        #lines with "exc" have excitations and osc strengths in difference indices
                        if (line.find("Exc.")) != -1:
                            #save excitation and osc strengths
                            #excitation
                            exc=line_split[3]
                            line_exc.append(exc)
                            #osc strength
                            osc=line_split[4]
                            line_exc.append(osc)
                        else:
                            #save excitation and osc strengths
                            #excitation
                            exc=line_split[2]
                            line_exc.append(exc)
                            #osc strength
                            osc=line_split[3]
                            line_exc.append(osc)   

                        
                        #filter here, check if excitation is in samia
                        #filter samia array down to energies that match this method, molecule, and tda status.
                        data_samia = df_samia[ (df_samia['Method'] == method) & (df_samia['TDA']==tda) & (df_samia['Molecule']==molecule_name) ]
                
                        #array of excitations
                        #capture all excitations that match those criteria in samia
                        excitations = data_samia['Energy'].values
                
                        
                        #if this excitation captured from the molgw output file does not match one of those, toss it out.
                        for excitation in excitations:

                            if float(exc) == float(excitation):
                                print("match", exc)
                                #add line_exc to overall dataframe array
                                parse_molgw_array.append(line_exc)

                    #stop searching once done with excitation energies
                    if line.find("Mean excitation energy") != -1:
                        break

            return parse_molgw_array

        #for output file "out.bse"
        extract_singlets_array=parse_molgw(input_path,self.molecule_name,self.tda,self.method,df_samia)
        #df_extract=pd.DataFrame(extract_singlets_array,columns=['Molecule','TDA','Method','Energy',"Osc."])

        return extract_singlets_array

    def filter_singlets(self,df_caroline,df_samia,molecule):
        """
        Check if the excitation energies match a value in Samia's excel data sheet.
        :param self
        :return none
        """
        
        #list all methods
        #methods=["0TZr","0TZ3","0TZh","0TZc","0TZp0","0TZp","evTZr","evTZ3","evTZh","evTZc","evTZp0","evTZp"]
        #tdas=["TDA","No_TDA"]

        #within samia df:
        #for method in methods:
        #    for tda in tdas:
        #        data = df_samia[ (df_samia['Method'] == method) & (df_samia['TDA']==tda) ]

    


        #for each method
            #for each tda status
                #for each molecule 
                    #check each excitation against df_caroline excitations that correspond on criteria
                    #if rounded singlet value matches p,arsed value to two decimal places:
                        #plug in oscill strength to df_samia

        #for m in methods:
        #    for t in tdas:
        #        #make a new data frame
        #        filtered_samia=df_samia[df_samia["Method"]== m & df_samia["TDA"] == t]
                
                #iterate through filtered_samia excitations
        #        for

            #check molecule name against samia's spreadsheet
            #check TDA status against samia's spreadsheet
            #check xcf-basis (method) against samia's spreadsheet
            #check excitation itself against samia's spreadsheet
            #if rounded singlet value matches p,arsed value to two decimal places:
                #add molecule (self.molecule()), tda status (self.tda_status()), excitation and oscillator strength to samia's data structure in new column for that entry)
            
        return None
        
        
############### A loose function ###########


############### Active Block ###############

#Load Samia's datasheet into a Pandas array
df_samia = pd.read_excel('/Users/CAMcKeon/python-env/env/Figures/OTRSH_2021/singlets_forMatching.xlsx',header=0,engine="openpyxl",sheet_name="test_aTZR")

#make an empt dataframe
df_caroline=pd.DataFrame(columns=['Molecule','TDA','Method','Energy',"Osc."])

#method
dir_split=(os.getcwd()).split("/")
method=dir_split[-1]

#List of all directories
subfolders = [ f.path for f in os.scandir(os.getcwd()) if f.is_dir() ]

#for each directory in this directory
for f in subfolders:
    #set mol_dir to name of directory
    #get the final characters after the last dash
    f_split=f.split("/")
    mol_dir=f_split[-1]

    #create an instance of osci_adder with molecule name and tda=0
    mol_object=osci_adder(mol_dir,"No_TDA",method)

    #run the extract_singlets function in osci_adder
    mol_array=mol_object.extract_singlets(mol_dir+"/OUT.bse",df_samia)
    
    #make dataframe for this molecule
    df_mol=pd.DataFrame(mol_array,columns=['Molecule','TDA','Method','Energy',"Osc."])

    df_caroline=df_caroline.append(df_mol,ignore_index = True)


    #if there is another directory folded under the molecule directory called "tda":
    if any(x.startswith('tda') for x in os.listdir(f)):
        #make another object
        mol_object_tda=osci_adder(mol_dir,"TDA",method)

        #run the extract_singlets function in osci_adder
        mol_array_tda=mol_object_tda.extract_singlets(mol_dir+"/tda/OUT.bse",df_samia)


        #make dataframe for this molecule
        df_mol_tda=pd.DataFrame(mol_array_tda,columns=['Molecule','TDA','Method','Energy',"Osc."])
        
        #add tda results to the same dataframe
        df_caroline=df_caroline.append(df_mol_tda,ignore_index = True)
        
        #test
        #print(mol_object.get_mol_name())
        #print(mol_object.get_tda())
    


    #Add TDA and non-TDA arrays to dataframe, to excel sheet, and close. 
    #print("array_mol",array_mol)
    #array_caroline.append(array_mol)

    
#print(df_caroline)
df_caroline.to_excel(method+"_output.xlsx")

# %%

# %%
