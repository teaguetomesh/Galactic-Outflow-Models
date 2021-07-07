import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

changefile = False
changedOnce = False
while True:
	if(changefile):
		whichFile = input("Choose galaxy: [0 = 1Zw18, 1 = haro11, 2 = KISSR1578, 3 = mrk1486,\n\t\t4 = NGC6090, 5 = NGC7714, 6 = SBS1415+437]: ")
		galaxies = ['1Zw18', 'haro11', 'KISSR1578', 'mrk1486', 'NGC6090', 'NGC7714', 'SBS1415+437']
		whichFileNum = int(float(whichFile))
		whichGalaxy = galaxies[whichFileNum]
		
		folderNames = ["Max Velocity - 200 Rad", "Max Velocity - Calc Rad", "Max Velocity - John\'s Rad"]
		dataFileNames = []
		howMany = input("How many models to plot? ")
		howMany = int(float(howMany))
		for i in range(howMany):
			folderName = input("Pick a folder: [Max Velocity - 200 Rad = 0, Max Velocity - Calc Rad = 1, Max Velocity - John\'s Rad = 2].\nIf not in a folder enter -1; New folder enter -2: ")
			folderName = int(float(folderName))
			if(folderName == -1):
				folderName = '-1'
			elif(folderName == -2):
				folderName = input('Folder name: ')
			else:
				folderName = folderNames[folderName]

			ucNum = input('Enter uc: ')
			
			if(folderName is '-1'):
				dataFileNames.append('DataFolder/ucInput' + ucNum + '.txt')
			else:
				dataFileNames.append('DataFolder/' + whichGalaxy + '/' + folderName + '/ucInput' + ucNum + '.txt')
	
	#Read in the data for each of the models
	dataFileNames = ['DataFolder/haro11/200,000pc/No shock/ucInput0.850.txt'
					 #'DataFolder/TermShocks 3 Variables/mrk1486/Single Wind Model/low xraylum cases/Beta 3.93 SFR 25/ucinput1.730.txt'
					 #'DataFolder/mrk1486/Max Velocity - Calc Rad/ucInput3.180.txt',
					 #'DataFolder/mrk1486/Max Velocity - John\'s Rad/ucInput0.995.txt'
					 # 'DataFolder/mrk1486/using Smallest Velocity v2/ucInput1.217.txt',
					 # 'DataFolder/mrk1486/using Smallest Velocity v2/ucInput1.247.txt'
					 ]
	#1Zw18, haro11, KISSR1578, mrk1486, NGC6090, NGC7714, SBS1415+437

	radius1, rho1, temp1, xraylum1, emissivity1, u1, cs1, integrand1 = [], [], [], [], [], [], [], []
	radius2, rho2, temp2, xraylum2, emissivity2, u2, cs2, integrand2 = [], [], [], [], [], [], [], []
	radius3, rho3, temp3, xraylum3, emissivity3, u3, cs3, integrand3 = [], [], [], [], [], [], [], []
	radius4, rho4, temp4, xraylum4, emissivity4, u4, cs4, integrand4 = [], [], [], [], [], [], [], []
	radius5, rho5, temp5, xraylum5, emissivity5, u5, cs5, integrand5 = [], [], [], [], [], [], [], []
	ucLegend = []
	calcVel = []

	for i in range(len(dataFileNames)):
		f = open(dataFileNames[i], 'r')

		#Read the first line of the simulation file to get rid of
		#the headers and get legend
		s = f.readline()
		ucLegend.append(s[82:99])
		print(ucLegend)
		#Then read in the data into the respective lists
		if(i == 0):
			while True:
				s = f.readline()
				if not s: break
				radius1.append(float(s[0:12])/(3.086*10**18))
				rho1.append(float(s[16:28]))
				temp1.append(float(s[32:44]))
				xraylum1.append(float(s[48:63]))
				emissivity1.append(float(s[63:79]))
				u1.append(float(s[79:95]))
				cs1.append(float(s[95:111]))
				integrand1.append(float(s[111:127]))
			f.close()

		elif(i == 1):
			while True:
				s = f.readline()
				if not s: break
				radius2.append(float(s[0:12])/(3.086*10**18))
				rho2.append(float(s[16:28]))
				temp2.append(float(s[32:44]))
				xraylum2.append(float(s[48:63]))
				emissivity2.append(float(s[63:79]))
				u2.append(float(s[79:95]))
				cs2.append(float(s[95:113]))
				integrand2.append(float(s[113:119]))
			f.close()
			
		elif(i == 2):
			while True:
				s = f.readline()
				if not s: break
				radius3.append(float(s[0:12])/(3.086*10**18))
				rho3.append(float(s[16:28]))
				temp3.append(float(s[32:44]))
				xraylum3.append(float(s[48:63]))
				emissivity3.append(float(s[63:79]))
				u3.append(float(s[79:95]))
				cs3.append(float(s[95:113]))
				integrand3.append(float(s[113:119]))
			f.close()
			
		elif(i == 3):
			while True:
				s = f.readline()
				if not s: break
				radius4.append(float(s[0:12])/(3.086*10**18))
				rho4.append(float(s[16:28]))
				temp4.append(float(s[32:44]))
				xraylum4.append(float(s[48:63]))
				emissivity4.append(float(s[63:79]))
				u4.append(float(s[79:95]))
				cs4.append(float(s[95:113]))
				integrand4.append(float(s[113:119]))
			f.close()
			
		elif(i == 4):
			while True:
				s = f.readline()
				if not s: break
				radius5.append(float(s[0:12])/(3.086*10**18))
				rho5.append(float(s[16:28]))
				temp5.append(float(s[32:44]))
				xraylum5.append(float(s[48:63]))
				emissivity5.append(float(s[63:79]))
				u5.append(float(s[79:95]))
				cs5.append(float(s[95:113]))
				integrand5.append(float(s[113:119]))
			f.close()
	
	#Get user input
	while True:
		xAxisLim1 = input('Enter x-axis lower limit (pc): ')
		xAxisLim2 = input('Enter x-axis upper limit (pc): ')
		xAxisLim1 = int(float(xAxisLim1))
		xAxisLim2 = int(float(xAxisLim2))
		if(xAxisLim1 < 0 or xAxisLim1 > xAxisLim2 or xAxisLim2 < 0):
			print('Invalid input')
		else: break
	# while True:
		# changeY = input('Change y-lim of Xray Lum? [0,1]: ')
		# if(changeY is '1'):
			# ylim1 = input('Enter upper limit (i.e. 1e41): ')
			# ylim1 = (float(ylim1))
			# changeY = True
			# changedOnce = True
			# break
		# else:
			# changeY = False
			# break
	
	legendNames = ["Haro 11"]
	
	###############################################################
	#PLOT 1
	
	# for i in range(len(radius1)):
		# if(radius1[i] < 200 and radius1[i+1]>200):
			# y1 = xraylum1[i]
		# if(radius1[i] < 500 and radius1[i+1]>500):
			# y2 = xraylum1[i]
		# if(radius1[i] < 1000 and radius1[i+1]>1000):
			# y3 = xraylum1[i]
	#plt.plot([200, 200], [0, y1], 'k--', lw=.5)
	#plt.plot([0, 200], [y1, y1], 'k--', lw=.5)
	
	#plt.plot([500, 500], [0, y2], 'k--', lw=.5)
	#plt.plot([0, 500], [y2, y2], 'k--', lw=.5)
	
	#plt.plot([1000, 1000], [0, y3], 'k--', lw=.5)
	#plt.plot([0, 1000], [y3, y3], 'k--', lw=.5)
	
	plt.plot(radius1, xraylum1, lw=2, label = legendNames[0])
	plt.plot(radius2, xraylum2, lw=2)
	plt.plot(radius3, xraylum3, lw=2)
	plt.plot(radius4, xraylum4, lw=2)
	plt.plot(radius5, xraylum5, lw=2)

	#if(changeY or changedOnce):
	plt.xscale('log')
	#plt.ylim([0, .3e39])
	plt.xlim([xAxisLim1, xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('X-ray Luminosity (erg/s)')
	plt.title('X-ray Luminosity within Radius r')
	#plt.text(50, .28e39, 'Lum within 1000pc = %.3e erg/s' % y3, fontsize=12)
	plt.legend(loc = 'upper left')
	plt.show()
	plt.close()

	###############################################################
	#PLOT 2
	plt.plot(radius1, emissivity1, lw=2)
	plt.plot(radius2, emissivity2, lw=2)
	plt.plot(radius3, emissivity3, lw=2)
	plt.plot(radius4, emissivity4, lw=2)
	plt.plot(radius5, emissivity5, lw=2)

	plt.xscale('log')
	#plt.ylim([0,.1e-29])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Emissivity (erg/(s*cm^3))')
	plt.title('X-ray Emissivity')
	plt.legend(legendNames, loc = 'upper right')
	plt.show()
	plt.close()

	###############################################################
	#PLOT 3
	plt.plot(radius1, u1, lw=2, label = ucLegend[0])
	plt.plot(radius2, u2, lw=2)
	plt.plot(radius3, u3, lw=2)
	plt.plot(radius4, u4, lw=2)
	plt.plot(radius5, u5, lw=2)
	
	ucVel = float(ucLegend[0][5:])
	for i in range(len(u1)):
		if(u1[i] <= ucVel and u1[i+1] > ucVel):
			x1 = radius1[i]
			break
	plt.plot([x1, x1], [0, ucVel], 'k--', lw=.5)
	plt.plot([0, x1], [ucVel, ucVel], 'k--', lw=.5)
			
	plt.xscale('log')
	#plt.ylim([0,5.5e+7])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Velocity (cm/s)')
	plt.title('Velocity of Flow')
	plt.legend(loc = 'upper right')
	plt.show()
	plt.close()

	###############################################################
	#PLOT 4
	# plt.semilogy(radius1, temp1)
	# plt.semilogy(radius2, temp2)
	# plt.semilogy(radius3, temp3)
	# plt.semilogy(radius4, temp4)
	# plt.semilogy(radius5, temp5)
	centTempLabel = "CentTemp = " + str(temp1[0]) + "K"
	plt.plot(radius1, temp1, lw=2, label = centTempLabel)
	plt.plot(radius2, temp2, lw=2)
	plt.plot(radius3, temp3, lw=2)
	plt.plot(radius4, temp4, lw=2)
	plt.plot(radius5, temp5, lw=2)

	plt.xscale('log')
	#plt.ylim([0,.6e7])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Temperature (K)')
	plt.title('Temperature of Flow')
	plt.legend(loc = 'upper right')
	plt.show()
	plt.close()

	###############################################################
	#PLOT 5
	# plt.semilogy(radius1, rho1)
	# plt.semilogy(radius2, rho2)
	# plt.semilogy(radius3, rho3)
	# plt.semilogy(radius4, rho4)
	# plt.semilogy(radius5, rho5)

	plt.plot(radius1, rho1, lw=2)
	plt.plot(radius2, rho2, lw=2)
	plt.plot(radius3, rho3, lw=2)
	plt.plot(radius4, rho4, lw=2)
	plt.plot(radius5, rho5, lw=2)

	plt.xscale('log')
	#plt.ylim([0,0.1e-26])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Density (particles/cm^3)')
	plt.title('Density of Flow')
	plt.legend(legendNames, loc = 'upper right')
	plt.show()
	plt.close()

	###############################################################
	#PLOT 6
	galaxyRadius = 22
	maxVelocity = 200
	for i in range(len(radius1)):
		calcVel.append(maxVelocity*(1-galaxyRadius/radius1[i])**0.5)
	plt.plot(radius1, calcVel)

	plt.ylim([0,200])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Velocity')
	plt.title('Calculate Velocity with Beta = 0.5')
	#plt.show()
	plt.close()
	
	###############################################################
	#PLOT 7

	#X-ray Lums at 200,000pc
	plt.scatter([0.02], [1.175e40], c='b', s = 100) #1Zw18
	plt.scatter([26.45], [2.893e41], c='g', s = 100) #haro11
	plt.scatter([3.72], [5.280e40], c='r', s = 100) #KISSR1578
	plt.scatter([3.6], [7.693e39], c='m', s = 100) #mrk1486
	plt.scatter([0.02], [1.222e41], c='c', s = 100) #SBS1415+437
	#X-ray lums at 1,000pc
	plt.scatter([0.02], [8.973e38], c='b', marker = 'D', s = 100) #1Zw18
	plt.scatter([26.45], [9.736e40], c='g', marker = 'D', s = 100) #haro11
	plt.scatter([3.72], [2.337e40], c='r', marker = 'D', s = 100) #KISSR1578
	plt.scatter([3.6], [3.685e39], c='m', marker = 'D', s = 100) #mrk1486
	plt.scatter([0.02], [2.533e38], c='c', marker = 'D', s = 100) #SBS1415+437
	
	#Set the correct colors to the correct galaxies
	blue_patch = mpatches.Patch(color='blue', label = "1Zw18")
	green_patch = mpatches.Patch(color='green', label = "haro11")
	red_patch = mpatches.Patch(color='red', label = "KISSR1578")
	magenta_patch = mpatches.Patch(color='m', label = "mrk1486")
	cyan_patch = mpatches.Patch(color='c', label = "SBS1415+437")
	
	#Plot the lines found in Zhang's paper
	plt.plot([0.01, 2.5e3], [1.2e37, 1e42], 'k-', lw=.5)
	plt.plot([0.01, 2.5e3], [1.2e38, 1e43], 'k-', lw=.5)
	plt.plot([0.2, 2.5e3], [1e37, 1e41], 'k-', lw=.5)
	
	plt.yscale('log')
	plt.xscale('log')
	plt.ylim([1e37, 2.5e43])
	plt.xlim([0, 2.5e3])
	plt.xlabel('SFR [$M_{\odot}/yr$]')
	plt.ylabel('Lx [$erg/s$]')
	plt.text(7e2, 9e42, 'fd=1', fontsize=12, rotation = 32)
	plt.text(6e2, 1e42, 'fd=0.1', fontsize=12, rotation = 33)
	plt.text(5e2, 1e41, 'fd=0.01', fontsize=12, rotation = 34)
	plt.text(2e-2, 2e42, "Circles: Lx @ 200,000pc\nDiamonds: Lx @ 1,000pc", fontsize = 14)
	plt.title('Galaxy Luminosity From Zhang et al')
	plt.legend(handles = [blue_patch, green_patch, red_patch, magenta_patch, cyan_patch], loc = "lower right")
	#plt.show()
	plt.close()
	
	###############################################################
	#PLOT 8
	plt.plot(radius1, integrand1, lw=2)
	plt.plot(radius2, integrand2, lw=2)
	plt.plot(radius3, integrand3, lw=2)
	plt.plot(radius4, integrand4, lw=2)
	plt.plot(radius5, integrand5, lw=2)

	plt.xscale('log')
	#plt.ylim([0,3.1e-24])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Integrand (erg/s/cm)')
	plt.title('Integrand before Integration')
	plt.legend(legendNames, loc = 'upper right')
	plt.show()
	plt.close()

	###############################################################
	#PLOT 9
	plt.plot(radius1, cs1, lw=2, label = "Sound Speed")
	plt.plot(radius1, u1, lw=2, label = "Wind Velocity")

	plt.xscale('log')
	#plt.ylim([0,3.1e-24])
	plt.xlim([xAxisLim1,xAxisLim2])
	plt.xlabel('r (pc)')
	plt.ylabel('Sound Speed and Velocity (cm/s)')
	plt.title('Comparing Sound and Wind Velocities')
	plt.legend(loc = 'upper right')
	plt.show()
	plt.close()

	break
	#plt.show()
	
	# keepGoing = input("To exit the program type \"exit\" (hit enter to plot again): ").lower()
	# if(keepGoing == "exit"):break
	# changefile = input('Do you want to change files? [0, 1]: ')
	# if(changefile is '0'): changefile = False
	# else: changeFile = True



