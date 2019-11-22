#parseGammaDFT.py
#Purpose: Given an output file with multiple DFT calculations, return the charge, SCF energy, and HOMO for all.

#############################
filePath="50seed-215.out"
#############################

#Read in all lines of file to reference later
m=open(filePath,"r")
allLines=m.readlines()
m.close()

with open (filePath,"r") as f:
    currentLine=1
    for line in f:
        if line.find
#How many calculations?

