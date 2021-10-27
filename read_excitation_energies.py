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
import os
from os import walk, listdir
from os.path import isfile,join
import glob
import xlsxwriter


def read_qchem(file_name):

	def read_file_for_ex(string_key):
	
		#initialize dataframe array
		dataframe_array=[]

		current_line=0

		#Read in all lines of file to reference later
		m=open(file_name,"r")
		allLines=m.readlines()
		m.close()

		with open (file_name,"r") as f:
			current_line=1
			for line in f:
				current_line+=1
				if line.find(string_key) != -1:
					section_line=current_line
					#iterate through all_lines starting at section_line, check if line contains -------
					for i in range(section_line+3,len(all_lines),1):
						if "-------" in all_lines[i]: 
							endsection_line=i			
							break
			#iterate through the anchors around TDDFT output section
			for j in range(section_line,endsection_line,1):
				#check if any line contains 'Singlet"
				if all_lines[j].find("Singlet") != -1:
				
					#create mini data array for that excitation
					ex_data=[]

					#pull out the excitation energy
					energy_line=all_lines[j-2]
					energy=float(energy_line[-7:-1])
					ex_data.append(energy)

					#pull out oscillator strength
					oscillator_line=all_lines[j+2]
					oscillator=float(oscillator_line[-13:-1])
					ex_data.append(oscillator)

					#append this excitation to overall dataframe array
					dataframe_array.append(ex_data)

		return dataframe_array
	
	#n=open(file_name+"-Energies.txt","w+")

	#write new file to create a mathematica-like list with brackets and commas between array values
	#for the energies
	#n.write("Singlets"+"={"+str(energies[0]))
	#for k in range(1,len(energies),1):
	#	n.write(","+str(energies[k]))
	#n.write("};\n")

	#and for the oscillators
	#n.write("Oscillators"+"={"+str(oscillators[0]))
	#for l in range(1,len(oscillators),1):
	#	n.write(","+str(oscillators[l]))
	#n.write("};\n")

	#report
	#print("\n\n\n"+str(len(energies))+" Singlets were found. Excitation energies and oscillator strengths were written to:\n"+file_name+"-Energies.txt\n\n\n")
	#close new file


	tddft_tda=read_file_for_ex("TDDFT/TDA Excitation")

	tddft_full=read_file_for_ex("TDDFT Excitation")


	return tddft_tda,tddft_full
	

def read_molgw(file_name):

	#null_array
	null_array=[]

	#initialize dataframe_array
	dataframe_array=[]

	#Read in all lines of file to reference later
	m=open(file_name,"r")
	allLines=m.readlines()
	m.close()

	current_line=0

	#open file
	with open (file_name,"r") as f:
		for line in f:
			current_line+=1
			
			#if an excitation is found
			if line.find("Exc.") != -1:

				#new array for that excitation
				ex_data=[]

				excitation_line=allLines[current_line-1]
				ex_line_split=excitation_line.split()

				#save excitation
				excitation=ex_line_split[3]
				ex_data.append(excitation)

				#save oscillator
				oscillator=ex_line_split[4]
				ex_data.append(oscillator)
		
				#save excitation to overall data frame
				dataframe_array.append(ex_data)


	#return array
	return dataframe_array,null_array



#read directory for array of output files
files=[]
for output_file in glob.glob("*.out"):
	files.append(output_file)
print(files)

#create new excel sheet for all file data
workbook=xlsxwriter.Workbook('excitation_data.xlsx')
workbook.close()

#is the file molgw or qchem?
#open file and check for q chem

for f in files:

	#create dataframe array for that file
	dataframe_array=[]

	m=open(f,"r")
	all_lines=m.readlines()
	m.close()

	current_line=1
	
	for line in all_lines:
		current_line+=1
		
		if line.find("Welcome to Q-Chem") != -1:
			file_type=0
			print("File",f,"\nFile Type",file_type,"\n\n")
			dataframe_array_1,dataframe_array_2=read_qchem(f)
			break

		elif line.find("MOLGW") != -1:
			file_type=1
			print("File",f,"\nFile Type",file_type,"\n\n")
			dataframe_array_1,dataframe_array_2=read_molgw(f)
			break
	

	df=pd.DataFrame(data=dataframe_array_1)
	df2=pd.DataFrame(data=dataframe_array_2)

	with pd.ExcelWriter('excitation_data.xlsx', engine='openpyxl', mode='a') as writer: 
		df.to_excel(writer,sheet_name = f)

	with pd.ExcelWriter('excitation_data.xlsx', engine='openpyxl', mode='a') as writer: 
		df2.to_excel(writer,sheet_name = f)	

