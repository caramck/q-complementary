######################
# Name: ProcessTuning.py
# Purpose: 
# Author: Caroline Anne McKeon, Feb 2020
######################

import os
import sys

###############
# FUNCTION parseFile
# ["fileName"; String of file to parse]
# Returns: j2 OR homoip
# Calls: calcJ2
def parseFile(fileName):

    #Load output file
    p=open(fileName,"r")
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
    return resultsAr





files=sys.argv[1]

#split each listed coordinate file into an array
if "," in files:
    filesAr=files.split(",")
print("filesAr: "+ str(filesAr))
print("filesAr length: "+str(len(filesAr)))

#open a file to save all results
f=open("results","w")

#write a header for the file
f.write("File name, SCF E Neutral, SCF E Anion, SCF E Cation, HOMO Neutral, HOMO Anion")

#parse each file for values and save it to the file
for x in filesAr:
    f.write("\n"+str(x))
    results=parseFile(x)
    for y in results:
        f.write(", "+str(y))


#save and close file
f.close()