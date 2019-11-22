#generateTuningScripts.py
#Purpose: In a directory, generate some given number of scripts optimizing a range of gamma from a given seed value with given coordinates

#############################
gammaList=["5","10","100","150","170","180","190","200","210","220","300","500"]
seedGamma=200
coords="SRBs0Coordinates.in"
newFileName="seed200-DIISGDM"
#############################

chargeRange=["0 1","1 2","-1 2"]

for i in range(0,int(len(gammaList))):
    #create new text file for this run
    newFileNameSpecific=str(newFileName+str(gammaList[i])+".in")
    with open(newFileNameSpecific,"w+") as n:
        #copy in SRB molecule coordinates and set up seed calculation
        n.write("$molecule\n0 1\n")
        with open(coords,"r") as f:
            for line in f:
                n.write(line)
        n.write("$end\n\n$rem\njobtype sp\nexchange gen\nlrc_dft 1\nomega "+str(seedGamma)+"\nbasis 6-31+g*\nrpa true\nscf_guess sad\nscf_algorithm diis_gdm\nsymmetry false\nsym_ignore true\nmax_scf_cycles 400\n$end\n\n$xc_functional\nX HF 0.2\nX wPBE 0.8\nC PBE 1.0\n$end\n\n")

        for g in range(0,3,1):
            charge=chargeRange[g]
            #set up subsequent calcs
            n.write("@@@\n\n$molecule\n"+charge+"\nread\n$end\n\n$rem\njobtype sp\nexchange gen\nlrc_dft 1\nomega "+gammaList[i]+"\nbasis 6-31+g*\nrpa true\nscf_guess read\nscf_algorithm diis_gdm\nsymmetry false\nsym_ignore true\nmax_scf_cycles 400\n$end\n\n$xc_functional\nX HF 0.2\nX wPBE 0.8\nC PBE 1.0\n$end\n\n")
