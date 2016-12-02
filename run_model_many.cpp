#include "model_without_prompts.h"
#include "model_without_prompts_v2.h"
#include "with_energy_scaled_radiative.h"
#include <iostream>
#include <stdio.h>
#include <list>
#include "gsl/gsl_math.h"
#include <fstream>
#include <math.h>
#include "store_data.h"
#include "xRayLum.h"
#include <iomanip>
#include <chrono>
#include <random>
using namespace std;

int main()
{
	int whichSim;
	cout << "Sim1 or Sim2? [1 or 2]: ";
	cin >> whichSim;
	
	if(whichSim == 1)
	{
		//Declare variables to pass to model_without_prompts
		double alpha, beta, SFR, uc, B1, mass, rad; 
		int shock;
		
		//Ask if looking at specific galaxy
		bool specificGal;
		int whichGalaxy;
		vector<string> galaxies = {"1Zw18", "haro11", "KISSR1578", "mrk1486", "NGC6090", "NGC7714", "SBS1415+437"};
		cout << "Specific Galaxy? [0, 1]: ";
		cin >> specificGal;
		if(specificGal)
		{
			cout << "Choose galaxy: [0 = 1Zw18, 1 = haro11, 2 = KISSR1578, 3 = mrk1486,"
					"\n\t\t4 = NGC6090, 5 = NGC7714, 6 = SBS1415+437]: ";
			cin >> whichGalaxy;
			switch(whichGalaxy)
			{
				case 0 :
						beta = 9.5;
						SFR = 0.02;
						mass = 7.2;
						rad = 200;
						break;
				case 1 :
						beta = 0.4301;
						SFR = 26.45;
						mass = 10.1;
						rad = 200;
						break;
				case 2 :
						beta = 0.920;
						SFR = 3.72;
						mass = 9.5;
						rad = 200;
						break;
				case 3 :
						beta = 0.48;
						SFR = 3.6;
						mass = 9.3;
						rad = 200;
						break;
				case 4 :
						beta = 0.09294;
						SFR = 25.15;
						mass = 10.7;
						rad = 200;
						break;
				case 5 :
						beta = 0.0721;
						SFR = 9.17;
						mass = 10.3;
						rad = 200;
						break;
				case 6 :
						beta = 12;
						SFR = 0.02;
						mass = 6.9;
						rad = 200;
						break;
			}
			alpha = 0;
			B1 = 3;
			shock = 2;
			cout << galaxies[whichGalaxy] << ":\n";
			cout << "Alpha: " << alpha << '\n';
			cout << "Beta: " << beta << '\n';
			cout << "SFR: " << SFR << '\n';
			cout << "Mass: " << mass << '\n';
			cout << "Rad: " << rad << '\n';
			cout << "B1: " << B1 << '\n';
			cout << "shock: " << shock << '\n';
			cout << "Enter velocity at critical radius: ";
			cin >> uc;
		}
		else
		{
			//Ask for values
			cout << "Enter alpha: ";
			cin >> alpha;

			cout << "Enter beta: ";
			cin >> beta;

			cout << "Enter SFR: ";
			cin >> SFR;
			
			cout << "Enter power of ten of mass of galaxy (9 for 10^9): ";
			cin >> mass;
			
			cout << "Enter velocity at critical radius: ";
			cin >> uc;
			
			cout << "Enter radius of mass and energy injection in parsecs: ";
			cin >> rad;

			cout << "Enter Magnetic Field in uG at 200pc: ";
			cin >> B1;

			cout << "Wind shocks? (0 = No; 1 = Yes, without B field; 2 = Yes, WITH B field)";
			cin >> shock;
		}

		//Open a file to store each run's data
		ofstream a_file ("simulation");
		if(a_file.is_open())
		{
			//Set up categories for file
			a_file << "Run #"<<"\t\t   "<<"Alpha"<<"\t\t"<<"Beta"<<"\t\t  "<<"SFR"<<"\t\t  "<<"Mass";
			a_file <<"\t     "<<"V@CritRad"<<"  "<<"BField@200pc"<<" "<<"Wind Shocks?";
			a_file <<"    "<<"CritRad"<<"\t\t"<<"uc"<<"\t     "<<"ShockForms?"<<" "<<"Bfield@Shock";
			a_file <<"   "<<"Shock Pos"<<"    "<<"CompRatio"<<"  "<<"Central Temp"<<"   "<<"X-ray Lum";
			a_file << endl;
		}
		else cout << "Unable to open file";
		
		a_file << scientific;

		//Create for loop to run many simulations at a time and write the results to the simulation file
		//for(int i = 0; i < 1; i++)
		int i=0;
		while(i<1)
		{
			//Call model_without_prompts and begin a run
			vector<double> callModel = model_without_prompts(alpha, beta, SFR, uc+i*0.03, B1, shock, mass, rad);
			
			//Use this if statement to stop code if there is an error
			if(callModel.size() == 1)
			{
				break;
			}
		
			//Write contents of callModel into simulation file
			if(i<9)
			{
				a_file << "Run #" << i+1 << ":    ";	
			}
			else if(i<99)
			{
				a_file << "Run #" << i+1 << ":   ";
			}
			else if(i<999)
			{
				a_file << "Run #" << i+1 << ":  ";
			}
			else{
				a_file << "Run #" << i+1 << ": ";
			}
			for(vector<double>::size_type i = 0; i<callModel.size(); i++)
			{
				a_file << callModel[i] << " ";
			}
			a_file << endl;
			
			i += 1;
		}
		
		a_file.close();
		
		return 0;
	}
	else
	{
		//Declare variables to pass to model_without_prompts
		double alpha, beta, SFR, uc, B1, mass, rad; 
		int shock;
		
		//xRayLum();
		
		//Ask for values
		cout << "Enter alpha: ";
		cin >> alpha;

		//cout << "Enter beta: ";
		//cin >> beta;

		//cout << "Enter SFR: ";
		//cin >> SFR;
		
		cout << "Enter power of ten of mass of galaxy (9 for 10^9): ";
		cin >> mass;
		
		cout << "Enter velocity at critical radius: ";
		cin >> uc;
		
		//cout << "Enter radius of mass and energy injection in parsecs: ";
		//cin >> rad;
		rad = 200;
		
		//cout << "Enter Magnetic Field in uG at 200pc: ";
		//cin >> B1;
		B1 = 3;
		
		cout << "Wind shocks? (0 = No; 1 = Yes, without B field; 2 = Yes, WITH B field)";
		cin >> shock;

		//Open a file to store each run's data
		cout << "Starting Loop \n\n";
		ofstream a_file ("termShock_sim2_data");
		if(a_file.is_open())
		{
			//Set up categories for file
/* 			a_file <<  setw(16) << "beta" << setw(16) << "crit rad" << setw(16) << "crit vel" << setw(16) 
					<< "ShockRad" << setw(16) << "Mach #" << setw(16)
					<< "AsymVel" << setw(16) << "Rho Shock" << setw(16) << "PostTemp";
			a_file << endl; */
		}
		else cout << "Unable to open file";
		
		a_file << scientific;

		//Run model with random variables and write data points to file
		for (int n = 0; n < 500000; n++)
		{
			SFR = (rand() % 200 + 1) * 0.1;
			beta = (rand() % 1500 + 1) * 0.01;

			cout << "\nSFR: " << SFR << "\tbeta: " << beta;
				
			//Call model_without_prompts and begin a run
			vector<double> callModel = model_without_prompts_v2(alpha, beta, SFR, uc, B1, shock, mass, rad);
			vector<double> callModel2 = model_without_prompts_v2(alpha, beta, SFR, uc, B1, 0, mass, rad);
			
			bool dontWrite = false;
				
			//Use this if statement to stop code if there is an error
			if(callModel.size() == 1)
			{
				cout << "callModel.size() == 1 ERROR";
				dontWrite = true;
			}
			
			if(callModel[14] < 0)
			{
				dontWrite = true;
			}
				
			//Write contents of callModel into termShock_sim2_data file
			vector<int> whichIndices = {1, 2, 14, 15, 13};
			/*
			1 = beta
			2 = SFR
			7 = crit rad
			8 = crit vel
			13 = cent temp
			14 = X-ray Lum
			15 = radius of shock
			16 = mach number
			17 = asymptotic velocity
			18 = density at shock
			19 = temp after shock
			*/
			if(!dontWrite)
			{
				for(vector<double>::size_type i = 0; i<whichIndices.size(); i++)
				{
					a_file << setw(16) << callModel[whichIndices[i]];
				}
				//a_file << setw(16) << callModel2[14];
				a_file << endl;	
			}
		}
		
		a_file.close();
		
		return 0;
	}
}
