#!/bin/bash

#Purpose: Shell script to automate PDB->Q-Chem->Mathematica readable file pipeline. Currently, accepts PDB file and produces text file with excitation energies and oscillator strengths for singlets. 

#list pdb files of interest, without (.pdb) file extension
fileList=(a b c)
charge="0 1"
method="pbe0"
basis="6-31+g*"
masterDirectory="Alexa488"

##############################################################
#create directories for each pdb file
for i in "${fileList[@]}"; do mkdir "$i"; done

#move each model to its own directory
for i in "${fileList[@]}"; do mv "$i".pdb "$i"; done 

#within each directory:
for i in "${fileList[@]}"; do
	:
 	cd /home/camckeon/Alexa488/ $i
	
	fileName=$i
	
	#Pass the pdb file name to the python file
	python /home/camckeon/Alexa488/readMD.py "$fileName" "$charge" "$method" "$basis" 

	#Run Q-Chem, submit geo optimization and DFT calculations as jobs (Qchem)
	run_qchem $i  16

	#How to check when Qchem run is done? This step cannot be completed until there is a full .out file.
	#Pull out excitation energies and oscillator strengths for singlets and write to a new file (Python)
	#python readExcitationEnergies.py "$fileName" 

done
