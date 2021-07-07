import numpy as np
import matplotlib.pyplot as plt

#Read in the data file
#Extra_Data
#1Zw18, haro11, KISSR1578, mrk1486, NGC6090, NGC7714, SBS1415+437
testfile = np.genfromtxt('DataFolder/haro11/New Cooling File/Extra_Data0.850.txt')

radius1 = testfile[:,0]
rho1 = testfile[:,1]
temp1 = testfile[:,2]
xraylum1 = testfile[:,3]
emissivity1 = testfile[:,4]
u1 = testfile[:,5]
cs1 = testfile[:,6]
integrand1 = testfile[:,7]
numdensity1 = testfile[:,8]
coolLambda1 = testfile[:,9]
radius1 = [val/(3.086*10**18) for val in radius1]

testfile2 = np.genfromtxt('DataFolder/haro11/200,000pc/Extra_Data.txt')

radius2 = testfile2[:,0]
rho2 = testfile2[:,1]
temp2 = testfile2[:,2]
xraylum2 = testfile2[:,3]
emissivity2 = testfile2[:,4]
u2 = testfile2[:,5]
cs2 = testfile2[:,6]
integrand2 = testfile2[:,7]
numdensity2 = testfile2[:,8]
coolLambda2 = testfile2[:,9]
radius2 = [val/(3.086*10**18) for val in radius2]


points = np.arange(len(radius1))
##############################################################################
#Get user input
# while True:
	# xAxisLim1 = input('Enter x-axis lower limit (pc): ')
	# xAxisLim2 = input('Enter x-axis upper limit (pc): ')
	# xAxisLim1 = int(float(xAxisLim1))
	# xAxisLim2 = int(float(xAxisLim2))
	# if(xAxisLim1 < 0 or xAxisLim1 > xAxisLim2 or xAxisLim2 < 0):
		# print('Invalid input')
	# else: break
xAxisLim1 = 0
xAxisLim2 = 200000	

clr = "blue"
galaxyName = "haro11"
##############################################################################

plt.figure(figsize=(10,10))

plt.plot(points, radius1, lw = 2, color = clr)

#Labels
plt.title("Radius at each index")
plt.xlabel("index")
plt.ylabel("Radius (pc)")
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
#plt.legend(loc='upper left')
#plt.show()
plt.close()
##############################################################################

plt.figure(figsize=(10,10))

plt.plot(radius1, numdensity1, lw = 2, color = clr, label = galaxyName)

#Labels
plt.title("Number Density")
plt.xlabel("Radius (pc)")
plt.ylabel("Number Density")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
plt.legend(loc='upper left')
plt.show()
plt.close()
##############################################################################

plt.figure(figsize=(10,10))

plt.plot(radius1, coolLambda1, lw = 2, color = clr, label = galaxyName)

#Labels
plt.title("Cooling Function")
plt.xlabel("Radius (pc)")
plt.ylabel("Radiative Loss Function  [$erg/(s*cm^3)$]")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
plt.legend(loc='upper left')
plt.show()
plt.close()
##############################################################################

fig, ax1 = plt.subplots()

ax1.plot(radius1, coolLambda1, lw = 2, color = clr)
ax1.set_xlabel("Radius (pc)")
ax1.set_ylabel("Radiative Loss Function  [$erg/(s*cm^3)$]", color = clr)
for tl in ax1.get_yticklabels():
	tl.set_color(clr)

ax2 = ax1.twinx()
ax2.plot(radius1, xraylum1, lw = 2, color = "green")
ax2.set_ylabel("X-ray Luminosity $[erg/s]$", color = "green")
for tl in ax2.get_yticklabels():
	tl.set_color("green")

#Labels
plt.title("Cooling Function with X-ray Luminosity")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
#plt.legend(loc='upper left')
plt.text(10, 1e41, 'Galaxy: '+galaxyName, fontsize=15)
plt.show()
plt.close()
##############################################################################

plt.figure(figsize=(10,10))

plt.plot(radius1, integrand1, lw = 2, color = "blue", label = "haro11")
plt.plot(radius2, integrand2, lw = 2, color = "red", label = "1Zw18")

#Labels
plt.title("Integrand")
plt.xlabel("Radius (pc)")
plt.ylabel("Integrand  [$erg/(s*cm)$]")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
plt.legend(loc='upper right')
#plt.show()
plt.close()
##############################################################################

fig, ax1 = plt.subplots()

ax1.plot(radius1, integrand1, lw = 2, color = clr)
ax1.set_xlabel("Radius (pc)")
ax1.set_ylabel("Integrand  [$erg/(s*cm)$]", color = clr)
for tl in ax1.get_yticklabels():
	tl.set_color(clr)

ax2 = ax1.twinx()
ax2.plot(radius1, xraylum1, lw = 2, color = "green")
ax2.set_ylabel("X-ray Luminosity $[erg/s]$", color = "green")
for tl in ax2.get_yticklabels():
	tl.set_color("green")

#Labels
plt.title("Integrand with X-ray Luminosity")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
#plt.legend(loc='upper left')
plt.text(7, 1e41, 'Galaxy: '+galaxyName, fontsize=15)
plt.show()
plt.close()
##############################################################################

fig, ax1 = plt.subplots()

ax1.plot(radius1, integrand1, lw = 2, color = clr)
ax1.set_xlabel("Radius (pc)")
ax1.set_ylabel("Integrand  [$erg/(s*cm)$]", color = clr)
for tl in ax1.get_yticklabels():
	tl.set_color(clr)

ax2 = ax1.twinx()
ax2.plot(radius1, coolLambda1, lw = 2, color = "green")
ax2.set_ylabel("Radiative Loss Function  [$erg/(s*cm^3)$]", color = "green")
for tl in ax2.get_yticklabels():
	tl.set_color("green")

#Labels
plt.title("Integrand with Cooling Function")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
plt.legend(loc='upper left')
plt.text(7, 3e-22, 'Galaxy: '+galaxyName, fontsize=15)
plt.show()
plt.close()
##############################################################################

plt.figure(figsize=(10,10))

plt.plot(radius1, coolLambda1, lw = 2, color = clr, label = "New Cooling")
plt.plot(radius2, coolLambda2, lw = 2, color = "green", label = "Old Cooling")

#Labels
plt.title("Cooling Functions")
plt.xlabel("Radius (pc)")
plt.ylabel("Radiative Loss Function  [$erg/(s*cm^3)$]")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
plt.legend(loc='upper left')
plt.show()
plt.close()
##############################################################################

plt.figure(figsize=(10,10))

plt.plot(radius1, xraylum1, lw = 2, color = clr, label = "New Lum")
plt.plot(radius2, xraylum2, lw = 2, color = "green", label = "Old Lum")

#Labels
plt.title("X-ray Luminosity")
plt.xlabel("Radius (pc)")
plt.ylabel("X-ray Luminosity $[erg/s]$")
plt.xscale('log')
#plt.ylim((-2,6))
plt.xlim(([xAxisLim1, xAxisLim2]))
plt.legend(loc='upper left')
plt.show()
plt.close()















