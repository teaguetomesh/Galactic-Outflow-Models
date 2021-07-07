import matplotlib.pyplot as plt
import numpy as np
import glob

#Get data
#data_table1 = np.genfromtxt('DataFolder/TermShocks 3 Variables/sfr_xraylum_w_shocks.txt')
#data_table2 = np.genfromtxt('DataFolder/TermShocks 3 Variables/sfr_xraylum_no_shocks.txt')

# numPoints = len(data_table1[:,0])
# numPoints = 1*(numPoints-1)
# beta1 = data_table1[:numPoints,0]
# SFR1 = data_table1[:numPoints,1]
# xRayLum1 = data_table1[:numPoints,2]

beta, SFR, xRayLum = [], [], []
shockRad, centTemp, critVel = [], [], []
num_models = 0
for file in glob.glob('DataFolder/TermShocks 3 Variables/haro/sfr_xraylum_beta*txt'):
	num_models = num_models+1
	
	model = np.genfromtxt(file)
	print(file)
	numPoints = 1*(len(model[:,0])-1)
	beta.append(model[:numPoints,0])
	SFR.append(model[:numPoints,1])
	xRayLum.append(model[:numPoints,2])
	shockRad.append(model[:numPoints,3])
	shockRadPC = [val/(3.086*10**18) for val in shockRad]
	centTemp.append(model[:numPoints,4])
	critVel.append(model[:numPoints, 5])

for model in range(num_models):
	badPoints = []
	for index in range(len(beta[model])):
		if(beta[model][index] > 1):
			badPoints.append(index)
	beta[model] = np.delete(beta[model], badPoints)
	SFR[model] = np.delete(SFR[model], badPoints)
	xRayLum[model] = np.delete(xRayLum[model], badPoints)
	shockRadPC[model] = np.delete(shockRadPC[model], badPoints)
	centTemp[model] = np.delete(centTemp[model], badPoints)
	critVel[model] = np.delete(critVel[model], badPoints)

##############################
# for model in range(num_models):
	# plt.scatter(SFR[model], xRayLum[model], s=50, c = beta[model], cmap = 'inferno')
	# clb = plt.colorbar()
	# clb.ax.set_title(r'$\beta$',fontsize=24)
	# plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
	# plt.xlabel('SFR',fontsize = 15)
	# plt.yticks(fontsize = 12)
	# plt.xticks(fontsize = 18)
	# plt.xlim(0, 10)
	# plt.ylim(0, 1e40)
	# plt.yscale('log')
	# plt.tight_layout()
	# if model is 10:
		# plt.title("Without Shocks")
	# else:
		# plt.title("With Shocks")
	# plt.show()
	
# bothTypesFile = np.genfromtxt('DataFolder/TermShocks 3 Variables/threeVarsWithShockRad.txt')
# betaBoth = bothTypesFile[:,0]
# SFRBoth = bothTypesFile[:,1]
# xRayLumWith = bothTypesFile[:,2]
# xRayLumWithout = bothTypesFile[:,4]
# shockRadCM = bothTypesFile[:,3]
# shockRadPC = [val/(3.086*10**18) for val in shockRadCM]

# badPoints = []
# for index in range(len(betaBoth)):
	# if(betaBoth[index] > 16 or shockRadPC[index] > 200000000 or SFRBoth[index] > 200 or xRayLumWith[index] > 1e100):
		# badPoints.append(index)
# betaBoth = np.delete(betaBoth, badPoints)
# SFRBoth = np.delete(SFRBoth, badPoints)
# xRayLumWith = np.delete(xRayLumWith, badPoints)
# xRayLumWithout = np.delete(xRayLumWithout, badPoints)
# shockRadPC = np.delete(shockRadPC, badPoints)

galSFR = 26.45
galXray = 4.54e+40
galBeta = 0.4301
galTemp = 3.683e+7

realValsS = [0.02, 3.72, 3.6, 0.02]
realValsX = [1.91E+37, 6.64e+39, 1.62e+39, 1.93e+37]
clrs = ['b', 'g', 'c', 'm']


#print(len(shockRadPC[0]))
for plotNum in range(1):
	if plotNum is 0:
		#xrays = xRayLumWith
		title = "Without Shock"
	else:
		xrays = xRayLumWithout
		title = "Without Shock"
		
	plt.scatter(SFR[0], xRayLum[0], s = 50, c = beta[0], cmap = 'inferno')
	clb = plt.colorbar()
	plt.scatter(galSFR, galXray, s = 75, c = 'r')
	for num in range(len(realValsS)):
		plt.scatter(realValsS[num], realValsX[num], s = 75, c = clrs[num])
	clb.ax.set_title(r'$\beta$',fontsize=24)
	plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
	plt.xlabel('SFR',fontsize = 15)
	plt.yticks(fontsize = 12)
	#plt.xticks(fontsize = 18)
	plt.xlim(0,100)
	plt.ylim(0,2e41)
	#plt.yscale('log')
	plt.tight_layout()
	plt.title(title)
	plt.show()
	plt.close()
	
	plt.scatter(SFR[0], xRayLum[0], s=50, c = shockRadPC[0], cmap = 'inferno')
	clb = plt.colorbar()
	clb.ax.set_title('Shock Radius [pc]',fontsize=12)
	plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
	plt.xlabel('SFR',fontsize = 15)
	plt.yticks(fontsize = 12)
	#plt.xticks(fontsize = 18)
	plt.xlim(0,100)
	plt.ylim(0,)
	#plt.yscale('log')
	plt.tight_layout()
	plt.title(title)
	#plt.show()
	plt.close()
	
	plt.scatter(SFR[0], shockRadPC[0], s=50, c = xRayLum[0], cmap = 'inferno')
	clb = plt.colorbar()
	clb.ax.set_title('X-ray Lum',fontsize=9)
	plt.ylabel('Radius of Shock [pc]',fontsize = 15)
	plt.xlabel('SFR',fontsize = 15)
	plt.yticks(fontsize = 12)
	#plt.xticks(fontsize = 18)
	#plt.xlim(0,20)
	plt.ylim(0,)
	#plt.yscale('log')
	plt.tight_layout()
	plt.title(title)
	#plt.show()
	plt.close()
	
	plt.scatter(shockRadPC[0], xRayLum[0], s=50, c = SFR[0], cmap = 'inferno')
	clb = plt.colorbar()
	clb.ax.set_title('SFR',fontsize=12)
	plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
	plt.xlabel('Shock Radius [pc]',fontsize = 15)
	plt.yticks(fontsize = 12)
	#plt.xticks(fontsize = 18)
	#plt.xlim(0,20)
	plt.ylim(0,)
	#plt.xscale('log')
	#plt.yscale('log')
	plt.tight_layout()
	plt.title(title)
	#plt.show()
	plt.close()
	
plt.figure(figsize=(10,10))
plt.scatter(SFR[0], shockRadPC[0], s = 50)
#Labels
plt.title("Radius of Shock vs. SFR")
plt.xlabel("SFR")
plt.ylabel("Radius of Shock [pc]")
#plt.xscale('log')
#plt.ylim((-2,6))
#plt.xlim(([xAxisLim1, xAxisLim2]))
#plt.legend(loc='upper left')
#plt.show()
plt.close()

plt.figure(figsize=(10,10))
plt.scatter(beta[0], shockRadPC[0], s = 50)
#Labels
plt.title("Radius of Shock vs. Beta")
plt.xlabel("Beta")
plt.ylabel("Radius of Shock [pc]")
#plt.xscale('log')
#plt.ylim((-2,6))
#plt.xlim(([xAxisLim1, xAxisLim2]))
#plt.legend(loc='upper left')
#plt.show()
plt.close()

plt.scatter(SFR[0], xRayLum[0], s = 50, c = beta[0]*SFR[0], cmap = 'inferno')
clb = plt.colorbar()
plt.scatter(galSFR, galXray, s = 75, c = 'r')
for num in range(len(realValsS)):
	plt.scatter(realValsS[num], realValsX[num], s = 75, c = clrs[num])
clb.ax.set_title(r'$\beta$*SFR',fontsize=15)
plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
plt.xlabel('SFR',fontsize = 15)
plt.yticks(fontsize = 12)
#plt.xticks(fontsize = 18)
plt.xlim(0,100)
plt.ylim(0,)
#plt.yscale('log')
plt.tight_layout()
plt.title(title)
plt.show()
plt.close()

plt.scatter(centTemp[0], xRayLum[0], s = 50, c = beta[0]*SFR[0], cmap = 'inferno')
clb = plt.colorbar()
plt.scatter(mrkTemp, mrkXray, s = 75, c = 'r')
clb.ax.set_title(r'$\beta$*SFR',fontsize=15)
plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
plt.xlabel('Central Temp (K)',fontsize = 15)
plt.yticks(fontsize = 12)
#plt.xticks(fontsize = 18)
plt.xlim(0,)
plt.ylim(0,)
#plt.yscale('log')
plt.tight_layout()
plt.title(title)
#plt.show()
plt.close()

plt.scatter(SFR[0], centTemp[0], s = 50, c = beta[0]*SFR[0], cmap = 'inferno')
clb = plt.colorbar()
plt.scatter(mrkSFR, mrkTemp, s = 75, c = 'r')
clb.ax.set_title(r'$\beta$*SFR',fontsize=15)
plt.ylabel('Central Temp (K)',fontsize = 15)
plt.xlabel('SFR',fontsize = 15)
plt.yticks(fontsize = 12)
#plt.xticks(fontsize = 18)
plt.xlim(0,100)
plt.ylim(0,)
#plt.yscale('log')
plt.tight_layout()
plt.title(title)
#plt.show()
plt.close()

plt.scatter(centTemp[0], shockRadPC[0], s = 50, c = beta[0]*SFR[0], cmap = 'inferno')
clb = plt.colorbar()
plt.scatter(mrkTemp, mrkXray, s = 75, c = 'r')
clb.ax.set_title(r'$\beta$*SFR',fontsize=15)
plt.ylabel('X-ray Luminosity within 200 kpc',fontsize = 15)
plt.xlabel('SFR',fontsize = 15)
plt.yticks(fontsize = 12)
#plt.xticks(fontsize = 18)
plt.xlim(0,)
plt.ylim(0,)
#plt.yscale('log')
plt.tight_layout()
plt.title(title)
#plt.show()
plt.close()

plt.scatter(critVel[0], SFR[0], s = 50, c = beta[0], cmap = 'inferno')
clb = plt.colorbar()
#plt.scatter(mrkTemp, mrkXray, s = 75, c = 'r')
clb.ax.set_title(r'$\beta$',fontsize=15)
plt.ylabel('SFR',fontsize = 15)
plt.xlabel('Critical Velocity',fontsize = 15)
plt.yticks(fontsize = 12)
#plt.xticks(fontsize = 18)
plt.xlim(0,5e7)
plt.ylim(0,)
#plt.yscale('log')
plt.tight_layout()
plt.title(title)
#plt.show()
plt.close()

plt.scatter(centTemp[0], critVel[0], s = 50, c = beta[0]*SFR[0], cmap = 'inferno')
clb = plt.colorbar()
#plt.scatter(mrkTemp, mrkXray, s = 75, c = 'r')
clb.ax.set_title(r'$\beta$*SFR',fontsize=15)
plt.ylabel('Critical Velocity',fontsize = 15)
plt.xlabel('Central Temp',fontsize = 15)
plt.yticks(fontsize = 12)
#plt.xticks(fontsize = 18)
plt.xlim(0,)
plt.ylim(0,5e7)
#plt.yscale('log')
plt.tight_layout()
plt.title(title)
#plt.show()
plt.close()

print(np.average(critVel[0]))
print(np.median(critVel[0]))
print(np.std(critVel[0]))

#print(len(beta[1]),len(SFR[1]),len(xRayLum[1]))
# print(beta[2][0])
# for n in range(len(beta[2])):
	# #print("in for loop")
	# #if(beta[1][n] > 10 and SFR[1][n] > 20 and SFR[1][n] < 30 and xRayLum[1][n] < .2e-8):
	# if(xRayLum[2][n] < 1e-8):
		# print(beta[2][n],'\t',SFR[2][n], xRayLum[2][n], n)

















