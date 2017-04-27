import matplotlib.pyplot as plt
import numpy as np

#Get data
data_table2 = np.genfromtxt('DataFolder/StepValue Data/Comparing 1pc to 1index/testStepData_ucInput1.730.txt')
data_table1 = np.genfromtxt('DataFolder/StepValue Data/Comparing 1pc to 1index/ucInput1.730.txt')
data_table3 = np.genfromtxt('DataFolder/StepValue Data/Comparing 1pc to 1index/Extra_Data.txt')

#numPoints = len(data_table1[:,0])
#numPoints = 1*(numPoints-1)
radius1cm = data_table1[:,0]
radius1 = [val/(3.086*10**18) for val in radius1cm]
xRayLum1 = data_table1[:,3]
emissivity1 = data_table1[:,4]
integrand1 = data_table1[:,7]
numDensity1 = data_table3[:,8]
coolLambda1 = data_table3[:,9]

radius2cm = data_table2[:,0]
radius2 = [val/(3.086*10**18) for val in radius2cm]
xRayLum2 = data_table2[:,3]
emissivity2 = data_table2[:,4]
integrand2 = data_table2[:,5]
numDensity2 = data_table2[:,1]
coolLambda2 = data_table2[:,2]

uc = 3.583057e+07


#############################################################################
#PLOTS
#############################################################################

plt.plot(radius1, xRayLum1, lw=2, color = 'blue', label = "Stepsize = 1 index")
plt.plot(radius2, xRayLum2, lw=2, color = 'red', ls = '--',  label = "Stepsize = 1 pc")

plt.xscale('log')
#plt.ylim([0,0.1e-26])
plt.xlabel('r (pc)')
plt.ylabel('Luminosity (erg/s)')
plt.title('MRK 1486: Effect of StepSize on X-ray Luminosity')
plt.legend(loc = 'lower right')
plt.show()
plt.close()

#############################################################################
#############################################################################

plt.plot(radius1, integrand1, lw=2, color = 'blue', label = "Stepsize = 1 index")
plt.plot(radius2, integrand2, lw=2, color = 'red', ls = '--',  label = "Stepsize = 1 pc")

plt.xscale('log')
#plt.ylim([0,0.1e-26])
plt.xlabel('r (pc)')
plt.ylabel('Integrand of Luminosity (erg/(s*cm))')
plt.title('MRK 1486: Effect of StepSize on Integrand')
plt.legend(loc = 'upper right')
plt.show()
plt.close()

#############################################################################
#############################################################################

plt.plot(radius1, emissivity1, lw=2, color = 'blue', label = "Stepsize = 1 index")
plt.plot(radius2, emissivity2, lw=2, color = 'red', ls = '--',  label = "Stepsize = 1 pc")

plt.xscale('log')
#plt.ylim([0,0.1e-26])
plt.xlabel('r (pc)')
plt.ylabel('Emissivity (erg/(s*cm^3))')
plt.title('MRK 1486: Effect of StepSize on Emissivity')
plt.legend(loc = 'upper right')
plt.show()
plt.close()

#############################################################################
#############################################################################
#############

plt.plot(radius1, numDensity1, lw=2, color = 'blue', label = "Stepsize = 1 index")
plt.plot(radius2, numDensity2, lw=2, color = 'red', ls = '--',  label = "Stepsize = 1 pc")

plt.xscale('log')
#plt.ylim([0,0.1e-26])
plt.xlabel('r (pc)')
plt.ylabel('Number Density (#/cm^3)')
plt.title('MRK 1486: Effect of StepSize on Number Density')
plt.legend(loc = 'upper right')
plt.show()
plt.close()

#############################################################################
#############################################################################
#############

plt.plot(radius1, coolLambda1, lw=2, color = 'blue', label = "Stepsize = 1 index")
plt.plot(radius2, coolLambda2, lw=2, color = 'red', ls = '--',  label = "Stepsize = 1 pc")

plt.xscale('log')
#plt.ylim([0,0.1e-26])
plt.xlabel('r (pc)')
plt.ylabel('Radiative Loss Function  [$erg/(s*cm^3)$]')
plt.title('MRK 1486: Effect of StepSize on Lambda')
plt.legend(loc = 'upper left')
plt.show()
plt.close()

#############################################################################
#############################################################################


