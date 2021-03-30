#generate_tuning_scripts.py
#Purpose: In a directory, generate some given number of scripts optimizing a range of gamma from a given seed value with given coordinates
import os,sys
import subprocess
import shutil


##########################################################
# Define file_parser object                              #
##########################################################

#constructor
class file_parser:
    """
   One instance of file parser parses all .out files in a directory.

    """

    #Constructor
    def __init__(self,file_name):
        """
        file_parser constructor 

        :param self
        :param file_name: string. file to parse
        :return none
        """

        #call parse file function
        self.file_name=file_name

    def find_files(self)
        """
        find_files: 

        :param self
        :return none
        """

    #TODO edit this and make it into a clean function
    def parse(self)


        """
        parse

        :param self
        :return none
        """

        file_name=self.file_name

        #Load output file
        p=open(file_name,"r")
        allLines=p.readlines()
        p.close()
        #SCF value array
        SCFe=[]
        #HOMO value array
        HOMOe=[]
        s=open(fileName,"r")

        # This iterating process could be more efficient - put more thought into this.
        # Create anchors for each section
        # Parse output file by job section: job 2 is neutral, job 3 is cation, job 4 is anion
        sectionAnchors=[]
        currentLine=1

        for line in s:
            #keep counter
            currentLine+=1
            #parse output file for job sections for all three jobs of interest
            if line.find("Running Job") !=-1:
                sectionAnchors.append(currentLine)
    
        s.close()
        #Total lines in output file
        sectionAnchors.append(len(allLines))

        currentLine=1
        #Pull out SCF and HOMO energies for each calculation of interest
        for i in range(2,5):
            #Look selectively in the range in file corresponding to that calculation

            #initiate homoArray outside of loop
            homoArray=[]

            for j in range(sectionAnchors[i-1],sectionAnchors[i]):
                currentLine+=1
                #search for SCF energy for that calculation
                if allLines[j].find("Total energy in the final basis set") != -1:
                    SCFline=str(allLines[j])
                    split=SCFline.split()
                    SCFe.append(float(split[-1]))

                # search for HOMO energy for that calculation

                if allLines[j].find("-- Virtual --") != -1:
                    HOMOline=str(allLines[j-1])
                    splitB=HOMOline.split()
                    homoArray.append(float(splitB[-1]))

            # Compare the saved HOMO energies, pick the highest if there are 2.
            if len(homoArray)==2:
                if homoArray[0]>homoArray[1]:
                    HOMOe.append(homoArray[0])
                else:
                    HOMOe.append(homoArray[1])
            else:
                HOMOe.append(homoArray[0]) 

        s.close()

        resultsAr=[SCFe[0],SCFe[1],SCFe[2],HOMOe[0],HOMOe[1]]    

##########################################################
# Parse each appropriate file                            #
##########################################################

#print header of table

#All files with ".out" should be parsed
#for each .out file make a file_parser class
#print gamma and results of array into a table


#put in a dataframe

#create a pyplot of homo+ip and lumo+ea and save



