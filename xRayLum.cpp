#include <iostream>
#include <stdio.h>
#include <list>
#include <fstream>
#include <math.h>
#include <string>
#include <vector>

using namespace std;

vector<double> xRayLum(double ucInput, double uc, double rad)
{
	//Open the data file
	ifstream file ("data");
	if(!file.is_open())
	{
		cout << "Unable to open data file";
	}
	
	//Take the data in the data file and place it into respective lists
	//Units:
	//		radius: cm
	//		rho: g/cm^3
	//		temp: K
	vector<double> radius, rho, temp, velocity, soundSpeed, junk3;
	double num;
	int i = 0;
	while (file >> num) {
		if(i == 0)
		{
			radius.push_back(num);
			i = 1;
		}
		else if(i == 1)
		{
			velocity.push_back(num);
			i = 2;
		}
		else if(i == 2)
		{
			soundSpeed.push_back(num);
			i = 3;
		}
		else if(i == 3)
		{
			rho.push_back(num);
			i = 4;
		}
		else if(i == 4)
		{
			junk3.push_back(num);
			i = 5;
		}
		else if(i == 5)
		{
			temp.push_back(num);
			i = 0;
		}
	}
	file.close();
	
	//Open the analyticCooling.txt file and get the xSpec data
	ifstream file2 ("analyticCooling.txt");
	if(!file2.is_open())
	{
		cout << "Unable to open analyticCooling.txt file";
	}
	
	//Units:
	//		xSpecT: K
	//		xSpecLambda: (erg/s)*cm^3
	vector<double> xSpecT, xSpecLambda, junk4;
	double num1;
	int index = 0;
	
	//Get rid of the first line of the file
	string firstline;
	getline(file2, firstline);
	
	while (file2 >> num1) {
		if(index == 0)
		{
			xSpecT.push_back(pow(10., num1));
			index = 1;
		}
		else if(index == 1)
		{
			junk4.push_back(num1);
			index = 2;
		}
		else if(index == 2)
		{
			xSpecLambda.push_back(pow(10., num1));
			index = 0;
		}
	}
	file2.close();
	
	//Constants
	double MASS = 1.021*pow(10,-24); //grams
	
	//Units: numParticles/cm^3
	vector<double> numDensity;
	for(vector<double>::size_type i=0; i<rho.size(); i++)
	{
		numDensity.push_back(rho[i]/MASS);
	}

	//Calculate the cooling function for each value of T in temp.
	//Must use the data given in xSpecT and xSpecLambda to estimate the
	//correct values for lambda at given T
	vector<double> coolLambda;
	
	//Loop through every term in the temp list
	double tempVal, leftT, rightT, leftLambda, rightLambda, estLambda;
	for(vector<double>::size_type i=0; i<temp.size(); i++)
	{
		tempVal = temp[i];
		//For each term in temp estimate a value for lambda by 
		//finding which two temperatures the temp term falls between in the xSpecT list.
		//Then find the average between the two lambdas that the two xSpecT temperatures
		//correspond to.
		for(vector<double>::size_type s=0; s<xSpecT.size()-1; s++)
		{
			leftT = xSpecT[s];
			rightT = xSpecT[s+1];
			if(tempVal >= leftT && tempVal <= rightT)
			{
				leftLambda = xSpecLambda[s];
				rightLambda = xSpecLambda[s+1];
				estLambda = (leftLambda + rightLambda)/2;
				break;
			}
		}
		coolLambda.push_back(estLambda);
	}
	
	//Numerically integrate the luminosity function:
	// 	Lx = integral((1.2)(0.71^2)*(n^2)*(r^2)*(lambda)dr) from 0 to infinity
	//Also integrate the luminosity function but without the r^2 term to give the emissivity
	vector<double> integrandAll;
	vector<double> emissivity;
	for(vector<double>::size_type i=0; i<radius.size(); i++)
	{
		integrandAll.push_back((1.2)*(pow(0.71, 2))*(pow(numDensity[i],2))*(pow(radius[i],2))*(coolLambda[i]));
		emissivity.push_back((1.2)*(pow(0.71, 2))*(pow(numDensity[i],2))*(coolLambda[i]));
	}
	
	//Calculate area under curve by adding up consecutive rectangles
	int i2 = 0, stepSize = 1;
	double totalArea = 0;
	double x1, x2, y2, tempArea, y1, yAvg;
	int vecSize = integrandAll.size();
	while(true)
	{
		x1 = radius[i2];
		x2 = radius[i2+stepSize];
		y2 = integrandAll[i2+stepSize];
		y1 = integrandAll[i2];
		yAvg = (y2+y1)/2;
		tempArea = (x2-x1)*(yAvg);
		totalArea += tempArea;
		i2 += stepSize;
		if((i2+stepSize) >= vecSize){break;}
	}
	cout<<"X-ray luminosity within 200,000pc: "<<totalArea<<" erg/s\n";
	
	vector<double> returnVec;
	returnVec.push_back(totalArea);
	
	//Create a vector that contains the value of the integral for different radii
	vector<double> integralSolved;
	double lumAtRadius;
	
	for(vector<double>::size_type i=0; i<radius.size(); i++)
	{
		lumAtRadius = 0;
		for(vector<double>::size_type s=0; s<i; s++)
		{
			lumAtRadius += (radius[s+1]-radius[s])*(0.5*((integrandAll[s+1])+(integrandAll[s])));
			if(isinf(lumAtRadius))
			{
				lumAtRadius = 0;
			}
		}
		integralSolved.push_back(lumAtRadius);
	}
	
	//Open a file to store each run's data
	string tempStr = to_string(ucInput);
	tempStr = tempStr.substr(0, 5);
	string fileName = "DataFolder/ucInput" + tempStr + ".txt";
	ofstream a_file (fileName);
	a_file << scientific;
	if(a_file.is_open())
	{
		//Set up categories for file
 		a_file << "   " << "Radius" << "\t\t    " << "rho" << "\t\t\t" << "Temperature" << "\t\t  ";
		a_file << "X-ray Lum" << "\t\t " << "Emissivity" << "\t\t     " << "u" << "\t\t         " << "cs";
		a_file << "\t\t\t" << "uc = " << uc;
		a_file << endl;
	}
	else cout << "Unable to open file";
	
	//To add the integrad to the file like before: add integrandAll[i]
	for(vector<double>::size_type i=0; i<radius.size(); i++)
	{
		a_file << radius[i] << "    " << rho[i] << "    " << temp[i] << "    ";
		a_file << integralSolved[i] << "    " << emissivity[i] << "    ";
		a_file << velocity[i] << "    " << soundSpeed[i] << "    " << integrandAll[i];
		a_file << endl;
	}
	a_file.close();
	
	//Find and print the maximum velocity
	double maxVel = -2; 
	double tempVel = -1;
	double radiusInParsec;
	double radiusLimit = 2.5*rad;
	for(vector<double>::size_type i=0; i<radius.size(); i++)
	{
		radiusInParsec = radius[i]/(3.086*pow(10,18));
		if(radiusInParsec > radiusLimit){break;}
		else
		{
			tempVel = velocity[i];
			if(tempVel > maxVel)
			{
				maxVel = tempVel;
			}
		}
	}
	maxVel = maxVel/100000;
	cout << "Max Velocity within " << to_string(radiusLimit).substr(0,6) << "pc: " << maxVel << " km/s\n";
	
	//Find and print the asymptotic velocity
	double asymVel = -2; 
	double tempVel2 = -1;
	double radiusInParsec2;
	double radiusLimit2 = 150000;
	for(vector<double>::size_type i=0; i<radius.size(); i++)
	{
		radiusInParsec2 = radius[i]/(3.086*pow(10,18));
		if(radiusInParsec2 > radiusLimit2){break;}
		else
		{
			tempVel2 = velocity[i];
			if(tempVel2 > asymVel)
			{
				asymVel = tempVel2;
			}
		}
	}
	asymVel = asymVel/100000;
	cout << "Aysmptotic Velocity: " << asymVel << " km/s\n";
	
	//Print the central temperature
	cout << "Central Temperature: " << temp[0] << " K\n";
	
	
	ofstream test_file ("DataFolder/Extra_Data.txt");
	test_file << scientific;
	for(vector<double>::size_type i=0; i<radius.size(); i++)
	{
		test_file << radius[i] << "    " << rho[i] << "    " << temp[i] << "    ";
		test_file << integralSolved[i] << "    " << emissivity[i] << "    ";
		test_file << velocity[i] << "    " << soundSpeed[i] << "    " << integrandAll[i] << "    ";
		test_file << numDensity[i] << "    " << coolLambda[i];
		test_file << endl;
	}
	test_file.close();
	
	return returnVec;
	
	//Add code to find the radius with 50% of the luminosity
}