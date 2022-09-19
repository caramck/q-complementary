#generate_tuning_scripts.py
#Purpose: In a directory, generate some given number of scripts optimizing a range of gamma from a given seed value with given coordinates
import os,sys
import subprocess
import shutil

##########################################################
# Define arguments from command line                     #
##########################################################

gamma_list=(sys.argv[1]).split(",")
seed_gam=sys.argv[2]
coords=sys.argv[3]
epsilon=sys.argv[4]


############################################################
#            Define generate_scripts class                 #
############################################################

#constructor
class generate_script:
    """
   Generate tuning scripts for OTRSH parameters.
    """

    #Constructor
    def __init__(self, gamma,seed_gam,coords,epsilon):
        """
        generate_scripts constructor 

        :param self
        :param gamma: int.
        :param seed_gam: seed gamma value for first script.
        :param coords: file in pathway containing coordinates.
        :return none
        """

        #static variables
        self.gamma=gamma
        self.seed_gam=seed_gam
        self.coords=coords
        self.epsilon=epsilon
        
        #designate new vars
        file_name=str("gamma"+str(gamma)+".in")
        
        self.file_name=file_name

    def create(self):
        """
        Create one Q Chem script with four dft calculations. 

        :param gamma: int.
        :param seed_gam: seed gamma value for first script.
        :param coords: file in pathway containing coordinates.
        :return none
        """
        charge_range=["0 1","1 2","-1 2"]

        gamma=self.gamma
        coords=self.coords
        seed_gam=self.seed_gam
        file_name=self.file_name
        epsilon=self.epsilon

        #define beta off epsilon
        alpha=float(0.2)
        beta=(float(1/float(epsilon)))-float(alpha)

        #create new text file for this run
        with open(file_name,"w+") as n:
            #copy in SRB molecule coordinates and set up seed calculation
            n.write("$molecule\n0 1\n")
            with open(coords,"r") as f:
                for line in f:
                    n.write(line)
            
            n.write("$end\n\n$rem\njobtype sp\nexchange gen\nlrc_dft 1\nomega "+str(seed_gam)+"\nbasis cc-pvtz\nrpa true\nscf_guess sad\nscf_algorithm diis_gdm\nsymmetry false\nsym_ignore true\nmax_scf_cycles 400\n$end\n\n$xc_functional\nX HF "+str(alpha)+"\nX wPBE "+str(beta)+"\nC PBE 1.0\n$end\n\n")
            for g in range(0,3,1):
                charge=charge_range[g]
                #set up subsequent calcs
                n.write("@@@\n\n$molecule\n"+charge+"\nread\n$end\n\n$rem\njobtype sp\nexchange gen\nlrc_dft 1\nomega "+str(gamma)+"\nbasis cc-pvtz\nrpa true\nscf_guess read\nscf_algorithm diis_gdm\nsymmetry false\nsym_ignore true\nmax_scf_cycles 400\n$end\n\n$xc_functional\nX HF "+str(alpha)+"\nX wPBE "+str(beta)+"\nC PBE 1.0\n$end\n\n")

        return None

    def submit(self):
        """
        submit Q-Chem script to cluster on MGF 

        :param file: str
        :return none
        """
        file_name=self.file_name

        command="run_qchem "+file_name+" 16"
        os.system(command)

        return None

    

############################################################
#            Generate and Submit Tuning Scripts            #
############################################################


for gamma in gamma_list:

    #create script object
    script=generate_script(gamma,seed_gam,coords,epsilon)

    #create script
    script.create()

    #submit script
    script.submit()
