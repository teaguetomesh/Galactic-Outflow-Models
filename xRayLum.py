import matplotlib.pyplot as plt
import sys
import math
import numpy
from statistics import mode

#Open the data file
file = open('data','r')
radius = []
rho = []
temp = []

#Take the data in the data file and place it into respective lists
#Units:
#		radius: cm
#		rho: particles/cm^3
#		temp: K
while True:
    s = file.readline()
    if not s: break
    radius.append(float(s[0:13]))#/(3.086*10**18))
    rho.append(float(s[39:52]))
    temp.append(float(s[65:78]))
file.close()

#Open the analyticCooling.txt file and get the xSpec data
file = open('analyticCooling.txt','r')
xSpecT =[]
xSpecLambda = []
#Units:
#		xSpecT: K
#		xSpecLambda: erg/s cm^3
xf=file.readline()
while True:
	xf=file.readline()
	if not xf: break
	xSpecT.append(10**(float(xf[2:7])))
	xSpecLambda.append(10**(float(xf[21:35])))
file.close()

#Constants
MASS = 1.021*10**-24 #grams

#Units: numParticles/cm^3
numDensity = [x/MASS for x in rho]
#nSubH = [0.71*x for x in numDensity]
#nSube = [1.2*x for x in nSubH]

#Calculate the cooling function for each value of T in temp.
#Must use the data given in xSpecT and xSpecLambda to estimate the 
#correct values for lambda at given T.
coolLambda = []

#Loop through every term in the temp list
for i in range(len(temp)):
	tempVal = temp[i]
	#For each term in temp estimate a value for Lambda by 
	#finding which two temperatures the temp term falls between in the xSpecT list.
	#Then find the average between the two lambdas that the two xSpecT temperatures 
	#correspond to.
	for s in range(len(xSpecT)-1):
		leftT = xSpecT[s]
		rightT = xSpecT[s+1]
		if(tempVal >= leftT and tempVal <= rightT):
			leftLambda = xSpecLambda[s]
			rightLambda = xSpecLambda[s+1]
			estLambda = (leftLambda + rightLambda)/2
			break
	coolLambda.append(estLambda)
#plt.plot(temp, coolLambda, "b")
#plt.show()

stepsizes, xraylums = [], []
#Create a while loop to allow for integration over many different ranges
#Step size corresponds to number of points skipped in radius list. 
#The average difference between points in the radius list is 21pc
stepsize = 1
while True:
	#Get user input
	if(True):
		while True:
			try:
				lowerBoundpc = float(input("Enter lower bound in parsecs: "))
				if(lowerBoundpc >= 0): break
				else: print("Must input an integer >= 0")
			except ValueError: print("Must input an integer")
		while True:
			try:
				upperBoundpc = float(input("Enter upper bound in parsecs: "))
				if(upperBoundpc >= lowerBoundpc): break
				else: print("Must input an integer > the lower bound")
			except ValueError: print("Must input an integer")
	
	#lowerBoundpc = 0
	#upperBoundpc = 3500
	
	#Convert upper and lower bounds into cm
	lowerBound = lowerBoundpc * (3.086*10**18)
	upperBound = upperBoundpc * (3.086*10**18)
	#Numerically integrate the luminosity function:
	#	Lx = integral((1.2)(0.71^2)*(n^2)*(r^2)*(lambda)dr) from 0 to infinity
	integrandAll, integrandCustom = [], []
	xAxisAll, xAxis = [], []
	newRadius, newRadiusAll = [], []
	#stepsize = 5
	for i in range(0, len(radius), stepsize):
		integrandAll.append((1.2)*(0.71**2)*(numDensity[i]**2)*(radius[i]**2)*(coolLambda[i]))
		xAxisAll.append(radius[i]/(3.086*10**18))
		newRadiusAll.append(radius[i])
		if(radius[i] >= lowerBound and radius[i] <= upperBound):
			integrandCustom.append((1.2)*(0.71**2)*(numDensity[i]**2)*(radius[i]**2)*(coolLambda[i]))
			xAxis.append(radius[i]/(3.086*10**18))
			newRadius.append(radius[i])
###############################################################################################################
	#Calculate area under curve by adding up consecutive rectangles		
	i, totalArea = 0, 0
	while True:
		x1 = newRadiusAll[i]
		x2 = newRadiusAll[i+1]
		y2 = integrandAll[i+1]
		tempArea = (x2-x1)*(y2)
		totalArea = tempArea + totalArea
		i = i+1
		if((i+1) >= len(integrandAll)): break
	print('X-ray luminosity within 200,000pc: {:.3e}' .format(totalArea),'erg/s')
	
	#Plot the integrand over the entire range for the radius
	if(True):
		plt.plot(xAxisAll, integrandAll, "b")
		plt.xlabel("Radius (pc)")
		plt.ylabel("X-ray Luminosity (erg/(cm*s)")
		plt.title("X-ray Emission of a Galactic Wind")
		ax = plt.subplot(111)
		plt.text(0.95, 0.95, 'X-ray luminosity within 200,000pc:\n{:.3e}erg/s' .format(totalArea),
			fontsize = 14, color = 'red', transform=ax.transAxes,
			horizontalalignment='right', verticalalignment='top')
		plt.show()
	
###############################################################################################################
	
	#Calculate the area under the curve by adding up consecutive rectangles
	i, area = 0, 0
	while True:
		x1 = newRadius[i]
		x2 = newRadius[i+1]
		y2 = integrandCustom[i+1]
		tempArea = (x2-x1)*(y2)
		area = tempArea + area
		i = i+1
		if((i+1)>=len(integrandCustom)): break
	percentArea = (area/totalArea)*100
	print('X-ray luminosity within',upperBoundpc,'pc: {:.3e}'.format(area), "erg/s")
	print("Percent of total within: %.2f%%" % (percentArea))
	
	#Plot the integrand over the range given by the user
	if(stepsize == 60 or stepsize == 80 or stepsize == 1):
		plt.plot(xAxis, integrandCustom, "b")
		plt.xlabel("Radius (pc)")
		plt.ylabel("X-ray Luminosity (erg/(cm*s)")
		plt.title("Integrand")
		ax = plt.subplot(111)
		plt.text(0.95, 0.95, 'X-ray luminosity within %s pc:\n{:.3e}erg/s'
			'\nPercent of total luminosity:\n%.2f%%\nStep Size: %.1f' 
			.format(area) % (upperBoundpc, percentArea, stepsize),
			fontsize = 14, color = 'red', transform=ax.transAxes,
			horizontalalignment='right', verticalalignment='top')
		plt.show()
	
###############################################################################################################

	#Create a vector that contains the value of the integral for different radii
	integralSolved = []

	for p in range(0, len(newRadius)):
		lumAtRadius = 0
		w = 0
		while(w < p):
			lumAtRadius = lumAtRadius + (newRadius[w+1]-newRadius[w])*(integrandCustom[w+1])
			if(numpy.isinf(lumAtRadius)):
				lumAtRadius = 0
			w = w + 1
		integralSolved.append(lumAtRadius)
	
	#Plot the luminosity over the range given by the user
	if(stepsize == 60 or stepsize == 80 or stepsize == 1):
		plt.xscale('log')
		plt.plot(xAxis, integralSolved, "b")
		plt.xlabel("Radius (pc)")
		plt.ylabel("X-ray Luminosity (erg/s)")
		plt.title("X-ray Luminosity")
		ax = plt.subplot(111)
		plt.text(0.95, 0.95, 'Step Size: %.1f' % (stepsize),
			fontsize = 14, color = 'red', transform=ax.transAxes,
			horizontalalignment='right', verticalalignment='top')
		plt.show()
	
###############################################################################################################
	
	stepsizes.append(stepsize)
	xraylums.append(totalArea)
	
	if(stepsize >= 100): break
	if(stepsize == 1): stepsize = 2
	else: stepsize = stepsize + 1
	
	# keepGoing = input('Enter "exit" to stop program; Press enter to begin again: ').lower()
	# if(keepGoing == "exit"): break

#Write the stepsize data to a file	
outf = open("stepSizeData.txt", "w")
for i in range(len(stepsizes)):
	outf.write("{:03d}  " .format(stepsizes[i]))
	outf.write("{}\n" .format(xraylums[i]))
outf.close()
plt.plot(stepsizes, xraylums, "b")
plt.xlabel("Step Size")
plt.ylabel("Total X-ray Luminosity")
plt.title("Effect of Step Size")
#plt.show()
plt.close()

#Find the mean, median, mode of the differences between consecutive elements in the radius list
# rDiffs = []
# for j in range(len(radius) - 1):
	# tempVal1 = radius[j]
	# tempVal2 = radius[j+1]
	# rDiffs.append(abs(tempVal1 - tempVal2))	
# print("Mean: ", numpy.mean(rDiffs)/(3.086*10**18))
# print("Median: ", numpy.median(rDiffs)/(3.086*10**18))
# print("Mode: ", mode(rDiffs)/(3.086*10**18))

###############################################################################################################

#Calculate Luminosity with increments of 1pc using averages
#Range of radius list goes from 5pc - 199980pc

# #Write the two lists to a file to use in MatLab
# matLab = open("integrandPoints.txt", "w")
# for i in range(len(newRadiusAll)):
	# matLab.write("{},  " .format(newRadiusAll[i]))
	# matLab.write("{}\n" .format(integrandAll[i]))
# matLab.close()

myRadii = []
radPC = 5
while True:
	radCM = radPC * (3.086*10**18)
	myRadii.append(radCM)
	radPC = radPC + 1
	if(radPC >= 3501): break
	
fullIntegrand = []
for i in range(len(radius)):
	fullIntegrand.append((1.2)*(0.71**2)*(numDensity[i]**2)*(radius[i]**2)*(coolLambda[i]))

myIntegrand = []
incrementSize = 100
for j in range(len(myRadii)):
	curRad = myRadii[j]
	for k in range(len(radius)-1):
		if(curRad >= radius[k] and curRad <= radius[k+1]):
			ystepValues, xstepValues = [], []
			deltaY = abs(fullIntegrand[k] - fullIntegrand[k+1])
			yincrement = deltaY/incrementSize
			deltaX = abs(radius[k] - radius[k+1])
			xincrement = deltaX/incrementSize
			for l in range(incrementSize+1):
				ystepValues.append(fullIntegrand[k] + l*yincrement)
				xstepValues.append(radius[k] + l*xincrement)
			for m in range(incrementSize):
				if(curRad >= xstepValues[m] and curRad <= xstepValues[m+1]):
					averageVal = abs(ystepValues[m] + ystepValues[m+1])/2
					myIntegrand.append(averageVal)
					break

myRadiiPC = []
for r in range(len(myRadii)):
	myRadiiPC.append(myRadii[r]/(3.086*10**18))
plt.plot(myRadiiPC, myIntegrand, "b")
plt.xlabel("Radius (pc)")
plt.ylabel("Integrand")
plt.title("Integrand with Steps = 1pc")
#plt.show()
plt.close()

#Now integrate up to each radius and plot to see how luminosity changes over radius
myLum = []

for p in range(0, len(myRadii)):
	myCurrLum = 0
	n = 0
	while(n < p):
		myCurrLum = myCurrLum + (myRadii[n+1]-myRadii[n])*(myIntegrand[n+1])
		if(numpy.isinf(myCurrLum)):
			myCurrLum = 0
		n = n + 1
	myLum.append(myCurrLum)

plt.plot(myRadii, myLum, "b")
plt.xlabel("Radius (pc)")
plt.ylabel("X-ray Luminosity (erg/s)")
plt.title("X-ray Luminosity with steps = 1pc")
#plt.show()
plt.close()





























