import matplotlib.pyplot as plt

f = open('simulation', 'r')
alpha = []
beta = []
sfr = []
mass = []
velAtCritRad = []
bfield = []
critrad = []
uc = []
shock = []
bfieldAtShock = []
shockPos = []
compRatio = []
centTemp = []

#Read the first line of the simulation file to get rid of
#the headers
s = f.readline()
#Then read in the data into the respective lists
while True:
	s = f.readline()
	if not s: break
	alpha.append(float(s[10:22]))
	beta.append(float(s[23:35]))
	sfr.append(float(s[36:49]))
	mass.append(10**(float(s[50:61])))
	velAtCritRad.append(float(s[62:75]))
	bfield.append(float(s[76:88]))
	critrad.append(float(s[101:114]))
	uc.append(float(s[115:127]))
	shock.append(float(s[128:139]))
	bfieldAtShock.append(float(s[140:153]))
	shockPos.append(float(s[154:166]))
	compRatio.append(float(s[166:178]))
	centTemp.append(float(s[179:192]))
f.close()


#Open the cool05_8.txt file
file = open('cool05_8.txt','r')
energy = []
coolingfunc = []

#Take the data in the cool05_8.txt file and place it
#into the correct lists
#Units:
#		energy: keV
#		coolingfunc: erg/s cm^3
while True:
	xf=file.readline()
	if not xf: break
	energy.append(float(xf[0:6]))
	coolingfunc.append(float(xf[6:17]))
while True:
	#Get user input
	while True:
		xName = input('Choose x-axis (Type "opt" to see list of options): ').lower()
		if(xName == "alpha" or xName == "beta" or xName == "sfr" or xName == "mass" or xName == "bfield" or
		xName == "critrad" or xName == "uc" or xName == "shock" or xName == "bfieldatshock" or
		xName == "shockpos" or xName == "compratio" or xName == "centtemp" or xName == "energy"
		or xName == "coolingfunc"): break
		elif(xName == "opt"): 
			print("Options:(alpha, beta, sfr, mass, bfield, critrad, uc, "
			"shock, bfieldAtShock, shockPos, compRatio, centTemp, energy, coolingfunc)")
		else: print("Invalid Input")
	while True:
		yName = input('Choose y-axis (Type "opt" to see list of options): ').lower()
		if(yName == "alpha" or yName == "beta" or yName == "sfr" or yName == "mass" or yName == "bfield" or
		yName == "critrad" or yName == "uc" or yName == "shock" or yName == "bfieldatshock" or
		yName == "shockpos" or yName == "compratio" or yName == "centtemp" or yName == "energy"
		or yName == "coolingfunc"): break
		elif(yName == "opt"): 
			print("Options:(alpha, beta, sfr, mass, bfield, critrad, uc, "
			"shock, bfieldAtShock, shockPos, compRatio, centTemp, energy, coolingfunc)")
		else: print("Invalid Input")
		
	#Assign the correct lists to xaxis and yaxis
	dataLists = [alpha, beta, sfr, mass, bfield, critrad, uc, shock,
	 bfieldAtShock, shockPos, compRatio, centTemp, energy, coolingfunc]
	nameList = ['alpha', 'beta', 'sfr', 'mass', 'bfield', 'critrad', 'uc', 'shock',
	 'bfieldatshock', 'shockpos', 'compratio', 'centtemp', 'energy', 'coolingfunc']
	for index in range(len(nameList)):
		if(xName == nameList[index]):
			xaxis = dataLists[index]
		if(yName == nameList[index]):
			yaxis = dataLists[index]
	
	#Plot the correct values
	plt.plot(xaxis, yaxis, 'b')
	#To hide the axis labelling stuff
	hide = True
	if(hide):
	#Label the x-axis
		if(xName=='alpha'): 
			plt.xlabel('Alpha Value')
			xTitle = "Alpha"
		if(xName=='beta'): 
			plt.xlabel('Beta Value')
			xTitle = "Beta"
		if(xName=='sfr'): 
			plt.xlabel('Star Formation Rate')
			xTitle = "SFR"
		if(xName=='mass'): 
			plt.xlabel('Mass of Galaxy (Solar Masses)')
			xTitle = "Mass of Galaxy"
		if(xName=='bfield'): 
			plt.xlabel('Magnetic Field Strength (Gauss)')
			xTitle = "B-Field"
		if(xName=='critrad'): 
			plt.xlabel('Critical Radius (pc)')
			xTitle = "Critical Radius"
		if(xName=='uc'): 
			plt.xlabel('Critical Velocity (cm/s)')
			xTitle = "Critical Velocity"
		if(xName=='shock'): 
			plt.xlabel('Shock Forms (Yes/No)')
			xTitle = "Shock Appearing"
		if(xName=='bfieldatshock'): 
			plt.xlabel('Magnetic Field at Shock (Gauss)')
			xTitle = "B-Field at Shock"
		if(xName=='shockpos'): 
			plt.xlabel('Shock Position (pc)')
			xTitle = "Shock Position"
		if(xName=='compratio'): 
			plt.xlabel('Compression Ratio')
			xTitle = "Compression Ratio"
		if(xName=='centtemp'): 
			plt.xlabel('Central Temp (K)')
			xTitle = "Central Temperature"
		if(xName=='energy'): 
			plt.xlabel('Energy (keV)')
			xTitle = "Energy"
		if(xName=='coolingfunc'): 
			plt.xlabel('Cooling Function (ergs/s cm^3)')
			xTitle = "Cooling Function"
	#Label the y-axis
		if(yName=='alpha'): 
			plt.ylabel('Alpha Value')
			yTitle = "Alpha"
		if(yName=='beta'): 
			plt.ylabel('Beta Value')
			yTitle = "Beta"
		if(yName=='sfr'): 
			plt.ylabel('Star Formation Rate')
			yTitle = "SFR"
		if(yName=='mass'): 
			plt.ylabel('Mass of Galaxy (Solar Masses)')
			yTitle = "Mass of Galaxy"
		if(yName=='bfield'): 
			plt.ylabel('Magnetic Field Strength (Gauss)')
			yTitle = "B-Field"
		if(yName=='critrad'): 
			plt.ylabel('Critical Radius (pc)')
			yTitle = "Critical Radius"
		if(yName=='uc'): 
			plt.ylabel('Critical Velocity (cm/s)')
			yTitle = "Critical Velocity"
		if(yName=='shock'): 
			plt.ylabel('Shock Forms (Yes/No)')
			yTitle = "Shock Appearing"
		if(yName=='bfieldatshock'): 
			plt.ylabel('Magnetic Field at Shock (Gauss)')
			yTitle = "B-Field at Shock"
		if(yName=='shockpos'): 
			plt.ylabel('Shock Position (pc)')
			yTitle = "Shock Position"
		if(yName=='compratio'): 
			plt.ylabel('Compression Ratio')
			yTitle = "Compression Ratio"
		if(yName=='centtemp'): 
			plt.ylabel('Central Temp (K)')
			yTitle = "Central Temperature"
		if(yName=='energy'): 
			plt.ylabel('Energy (keV)')
			yTitle = "Energy"
		if(yName=='coolingfunc'): 
			plt.ylabel('Cooling Function (ergs/s cm^3)')
			yTitle = "Cooling Function"
	plt.title('%s vs %s'%(yTitle, xTitle))
	plt.show()
	
	keepGoing = input("To exit the program type \"exit\" (hit enter to plot again): ").lower()
	if(keepGoing == "exit"):break
