#include "model_without_prompts.h"
#include "with_energy_scaled_radiative.h"
#include <iostream>
#include <stdio.h>
#include <list>
#include "gsl/gsl_math.h"
#include <fstream>
#include <math.h>
#include "store_data.h"
#include "xRayLum.h"

using namespace std;

int main()
{
	//Declare variables to pass to model_without_prompts
	double alpha, beta, SFR, uc, B1, mass; 
	int shock;
	
	//xRayLum();
	
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

    cout << "Enter Magnetic Field in uG at 200pc: ";
    cin >> B1;

    cout << "Wind shocks? (0 = No; 1 = Yes, without B field; 2 = Yes, WITH B field)";
    cin >> shock;

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
		vector<double> callModel = model_without_prompts(alpha, beta, SFR, uc-i*.01, B1, shock, mass);
	
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
