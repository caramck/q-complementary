#calculateJ2.py
#Purpose: Calculate J^(2) given total energies HOMOs from anion, cation, and neutral molecular DFT calculations
#Caroline McKeon, November 2019
#edit

###############INPUT#####################
#SCF Energies: Neutral, Anion, Cation
eSCFneutral=float(-2690.7594)
eSCFanion=float(-2691.3349)
eSCFcation=float(-2690.2259)

#HOMO Energies: Neutral, Anion
eHOMOneutral=float(-0.5943)
eHOMOanion=float(-0.4905)

#########################################


#Define Ionization Potentials.
IPneutral=float(eSCFcation-eSCFneutral)
IPanion=float(eSCFneutral-eSCFanion)

#Calculate.
##J^(2)converted to eV
jSq=(27.211)*(27.211)*(((abs(eHOMOneutral+IPneutral))**2)+((abs(eHOMOanion+IPanion)))**2)

##HOMO+IP
jAnion=(27.211)*((abs(eHOMOanion+IPanion)))

##LUMO+EA
jNeutral=(27.211)*((abs(eHOMOneutral+IPneutral)))

#Report.
print("\n\nJ^(2) is "+str(jSq)+"\nJ(N+1) is "+str(jAnion)+"\nJ(N) is "+str(jNeutral)+"\n\n")

##Bound or unbound?
if jAnion>0:
    print("The anion is unbound. Minimize J(N) instead of J^(2).\n\n")
