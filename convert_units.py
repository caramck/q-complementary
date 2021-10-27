# convert_units.py
# Purpose: for an input file with atomic coordinates in Bohrs, convert to angstroms
#   and generate a new input file.
# October 2021
# Caroline McKeon


import os,sys
import subprocess
import shutil

############################################################
#          convert from bohr to angstrom                   #
############################################################

def bohr_to_angstrom(bohr_number):
    """
    calc_lumo_ea: find difference between given lumo and ea values
    :return none
    """
    angstrom_number=bohr_number*(0.529177)

    return angstrom_number


##########################################################
#           Define arguments from command line           #
##########################################################

file_name=(sys.argv[1])

############################################################
#            conversion                                    #
############################################################

#read input file
p=open(file_name,"r")
all_lines=p.readlines()
p.close()

#store each line as an array with information about atom
bohr_array=[]
for line in all_lines:
    atom_array=[]
    atom_array=line.split()
    
    #get rid of exponent "E" in coordinates
    for i in range(1,4):
        if str(atom_array[i]).find("E") != -1:
            atom_array[i]=str("0.0")

    bohr_array.append(atom_array)


print("atom_array",atom_array)
print("bohr_array",bohr_array)

#convert the coordinates from bohr to angstroms and store in new array
angstrom_array=[]
for a_array in bohr_array:
    temp_b=[]
    temp_a=[]
    temp_b=a_array

    #append atom identifier without adjustment
    temp_a.append(temp_b[0])

    #convert each bohr coordinate to angstrom
    temp_a.append(str(bohr_to_angstrom(float(temp_b[1]))))
    temp_a.append(str(bohr_to_angstrom(float(temp_b[2]))))
    temp_a.append(str(bohr_to_angstrom(float(temp_b[3]))))

    #add this atom converted to angstrom to the overall angstrom array
    angstrom_array.append(temp_a)


#create a new file
f = open("a_"+file_name, "x")

#read out converted array into new file and close
for atom in angstrom_array:
    f.write("\n"+str(atom[0])+ "  "+str(atom[1])+"  "+str(atom[2])+"  "+str(atom[3]))

f.write("\n\n")
f.close()




