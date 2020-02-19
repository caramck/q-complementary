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


scfN=[]
scfA=[]
scfC=[]
homoN=[]
homoA=[]
names=[]

#parse each file for values and save it to the file
for x in filesAr:
    results=parseFile(x)
    print("x: "+str(x))
    #save specific lists
    names.append(str(x))
    print("names: "+str(names))
    scfN.append(results[0])
    scfA.append(results[1])
    scfC.append(results[2])
    homoN.append(results[3])
    homoA.append(results[4])
    

f.write("Names={"+str(names[0]))
for j in range(1,len(filesAr)):
    f.write(","+str(names[j]))
f.write("}")

f.write("\nSCFN={"+str(scfN[0]))
for j in range(1,len(filesAr)):
    f.write(","+str(scfN[j]))
f.write("}")

f.write("\nSCFA={"+str(scfA[0]))
for j in range(1,len(filesAr)):
    f.write(","+str(scfA[j]))
f.write("}")

f.write("\nSCFC={"+str(scfC[0]))
for j in range(1,len(filesAr)):
    f.write(","+str(scfC[j]))
f.write("}")

f.write("\nHOMON={"+str(homoN[0]))
for j in range(1,len(filesAr)):
    f.write(","+str(homoN[j]))
f.write("}")
    
f.write("\nHOMOA={"+str(homoA[0]))
for j in range(1,len(filesAr)):
    f.write(","+str(homoA[j]))
f.write("}")

#save and close file
f.close()