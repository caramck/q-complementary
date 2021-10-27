#%%
# #read_excitation_energies_excel.py
#Purpose: Read out the TDDFT Singlet Excitation Energies and oscillator strengths and write them as separate lists in an output file.  
#Call script with file_name.

#figure out how to pass something in on the command line that will set the filePath variable
#keep this file stored in some specific place, call on it to perform this routine and save output to a passed in directory

#dataframe format: [['a','b'],['c','d']]
#each entry ['a','b'] is a row
#each entry will be an excitation

#allow python script to use shell arguments
import sys
import pandas as pd

#open file
file_name=sys.argv[1]

#Read in all lines of file to reference later
m=open(file_name+".out","r")
all_lines=m.readlines()
m.close()

#Search for TDDFT Excitation Energies string
with open (file_name+".out","r") as f:
    #create overall dataframe array
    dataframe_array=[]
    current_line=1

    for line in f:
        current_line+=1
        print("here")
        if line.find("Excitation Energies") != -1:
            print("here")
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
            ex_data.append(file_name)

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

    #write dataframe to excel sheet
    df=pd.DataFrame(data=dataframe_array)
    df.to_excel(file_name+".xlsx")
        



# %%
