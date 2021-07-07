import matplotlib.pyplot as plt
import numpy as np

#Get data
data_table1 = np.genfromtxt('DataFolder/Investigating new cooling file/oldCooling.txt')
data_table2 = np.genfromtxt('DataFolder/Investigating new cooling file/newCooling.txt')

tempOldlog = data_table1[:,0]
tempOld = [10**val for val in tempOldlog]

lambdaOldlog = data_table1[:,2]
lambdaOld = [10**val for val in lambdaOldlog]

tempNewlog = data_table2[:,0]
tempNew = [10**val for val in tempNewlog]

lambdaNewlog = data_table2[:,2]
lambdaNew = [10**val for val in lambdaNewlog]

#--------------------------------------------

plt.plot(tempOldlog, lambdaOldlog, lw=2, c='r', label = "Old File")
plt.plot(tempNewlog, lambdaNewlog, lw=2, c='b', label = "New File")

#plt.ylim([0,0.1e-26])
plt.xlabel('log(T)')
plt.ylabel('log(lambda')
plt.title('Cooling values used for interpolation')
plt.legend(loc = 'lower right')
plt.show()
plt.close()

#--------------------------------------------

plt.plot(tempOldlog, lambdaOldlog, lw=2, c='r', label = "Old File")

plt.xlabel('log(T)')
plt.ylabel('log(lambda')
plt.title('Cooling values used for interpolation')
plt.legend(loc = 'lower right')
plt.show()
plt.close()

#--------------------------------------------

plt.plot(tempNewlog, lambdaNewlog, lw=2, c='b', label = "New File")

plt.xlabel('log(T)')
plt.ylabel('log(lambda')
plt.title('Cooling values used for interpolation')
plt.legend(loc = 'lower right')
plt.show()
plt.close()

