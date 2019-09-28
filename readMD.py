#ReadMD.py
#Purpose: Take a PDB file as input and run a geo opt and DFT calc in Q-chem. 
#Call script with fileName, charge, method, and basis.

#Define variables
import sys
filePath=sys.argv[1]
charge=sys.argv[2]
method=sys.argv[3]
basis=sys.argv[4]

#Create q-chem geometry optimization file
f= open(filePath+".in","w+")
#Write beginning of Q-chem file
f.write("!Geometry Optimization for "+filePath+"\n"+"$molecule"+"\n"+charge+"\n") 
with open (filePath+".pdb", "r") as fileHandler:
        # Read each line in loop, check for HETATM
        for line in fileHandler:
       		 if line.find("HETATM") != -1:
			#save every line containing HETATM to a new file, remove unnecessary info
			f.write(line[13:14]+line[31:55]+"\n")
#Write Ge-Opt part of Q-Chem file
f.write("$end"+"\n\n"+"$rem\njobtype opt\ngeom_opt_print 5\ngeom_opt_symflag true\nmethod "+method+"\nbasis "+basis+"\nscf_convergence 8\nthresh 14\nsymmetry false\nsym_ignore true\nscf_print 1\nscf_final_print 1\n$end" )

#Write DFT part of Q-Chem file
f.write("\n\n@@@\n\n\n$molecule\nread\n$end\n\n$rem\njobtype sp\nrpa true\ncis_n_roots 10\nmethod "+method+"\nbasis "+basis+"\nmax_scf_cycles 100\nscf_guess sad\nscf_algorithm diis\nscf_convergence 8\nthresh 14\nsymmetry false\nsym_ignore true\nmem_static 2000\nmem_total 8000\nscf_print 1\nscf_final_print 1\nprint_orbitals 10\nCISTR_PRINT true\nCIS_AMPL_ANAL true\nPRINT_GENERAL_BASIS true\nnto_pairs 2\nsolvent_method pcm\n$end\n\n$pcm\ntheory iefpcm\nprintlevel 0\n$end")

#Close files
f.close()
fileHandler.close()
