#readExcitationEnergies.py
#Purpose: Read out the TDDFT Singlet Excitation Energies and oscillator strengths and write them as separate lists in an output file.  
#Call script with fileName.

#figure out how to pass something in on the command line that will set the filePath variable
#keep this file stored in some specific place, call on it to perform this routine and save output to a passed in directory

#dataframe format: [['a','b'],['c','d']]
#each entry ['a','b'] is a row
#each entry will be an excitation

#allow python script to use shell arguments
import sys
import pandas as pd

fileName=sys.argv[1]
excel=sys.argv[2]

#initialize oscillator and energies array and file path for dft outout
energies=[]
oscillators=[]

#initialize excel array


#Read in all lines of file to reference later
m=open(fileName+".out","r")
allLines=m.readlines()
m.close()

#Search for TDDFT Excitation Energies string
with open (fileName+".out","r") as f:
	currentLine=1
	for line in f:
		currentLine+=1
		if line.find("TDDFT Excitation Energies") != -1:
			sectionLine=currentLine
			#iterate through allLines starting at sectionline, check if line contains -------
			for i in range(sectionLine+3,len(allLines),1):
				if "-------" in allLines[i]: 
					endSectionLine=i			
					break
	#iterate through the anchors around TDDFT output section
	for j in range(sectionLine,endSectionLine,1):
		#check if any line contains 'Singlet"
		if allLines[j].find("Singlet") != -1:
			#pull out the excitation energy
			energy=allLines[j-2]
			energies.append(float(energy[-7:-1]))
			#pull out oscillator strength
			oscillator=allLines[j+2]
			print("Oscillator variable: "+oscillator)
			oscillators.append(float(oscillator[-13:-1]))

#create energies output file
n=open(fileName+"-Energies.txt","w+")

#write new file to create a mathematica-like list with brackets and commas between array values
#for the energies
n.write("Singlets"+"={"+str(energies[0]))
for k in range(1,len(energies),1):
	n.write(","+str(energies[k]))
n.write("};\n")

#and for the oscillators
n.write("Oscillators"+"={"+str(oscillators[0]))
for l in range(1,len(oscillators),1):
	n.write(","+str(oscillators[l]))
n.write("};\n")

#report
print("\n\n\n"+str(len(energies))+" Singlets were found. Excitation energies and oscillator strengths were written to:\n"+fileName+"-Energies.txt\n\n\n")
#close new file
n.close()
