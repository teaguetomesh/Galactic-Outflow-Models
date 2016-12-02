#include "with_energy_scaled_radiative.h"
#include <stdio.h>
#include <list>
#include "model_without_prompts.h"
#include "model_without_prompts_v2.h"
#include <vector>
#include <iostream>
using namespace std;

//This is a static vector that will hold the different data values
//generated in with_energy_scaled_radiative.cpp
static vector<double> calculatedData(6);

//This method receives the data from with_energy_scaled_radiative
//and places it into the calculatedData vector
void store_data(double critRad, double critVel, double shockPresent, double Bfield,
						double shockPos, double compRatio)
{
	vector<double> tempVec = {critRad, critVel, shockPresent, Bfield, shockPos, compRatio};
	
	for(vector<double>::size_type i = 0; i<6; i++)
	{
		calculatedData[i] = tempVec.at(i);
		//printf("%f\n",calculatedData[i]);
	}
}

//This method combines the vector of data from model_without_prompts.cpp
//and the calculatedData vector
vector<double> complete_data(vector<double> incompleteData)
{
	//cout<<"Inside complete_data\n";
	for(vector<double>::size_type i=7; i<incompleteData.size()-1; i++)
	{
		incompleteData[i] = calculatedData.at(i-7);
	}
/* 	for(vector<double>::size_type i=0; i<incompleteData.size(); i++)
	{
		cout<<incompleteData[i]<<"\n";
	} */
	//cout<<"Exiting complete_data\n";
	return incompleteData;
}

//Adds the central temp to the end of the data vector
vector<double> add_Temp(vector<double> incompleteData, double centTemp)
{
	int lastIndex = incompleteData.size()-1;
	incompleteData[lastIndex] = centTemp;
	return incompleteData;
}