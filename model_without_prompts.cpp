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

vector<double> model_without_prompts(double alpha, double beta, double SFR, double uc,
									 double B1, int shock, double mass)
{
	const double P_IGM = gsl_pow_int(10,-14);
    const double G = 6.6726 * gsl_pow_int(10, -8);
    const double KB = 1.3807 * gsl_pow_int(10, -16); 
    const double M_MASS = 1.021 * gsl_pow_int(10, -24);
    double gamma, m, m_h, a, rad;
  
    //cout << "Enter alpha: ";
    //cin >> alpha;

    //cout << "Enter beta: ";
    //cin >> beta;

    //cout << "Enter SFR: ";
    //cin >> SFR;

    //get gamma value of 4/3 or 5/3 from user
    int in;
    //cout << "Enter gamma (5 for 5/3, 4 for 4/3): ";
    //cin >> in;
    in = 5;
    if (in == 5)
    {
        gamma = 5. / 3.;
    }
    else if (in == 4)
    {
        gamma = 4. / 3.;
    }
    else
    {
        fprintf(stderr, "Error in gamma input.");
		vector<double> empty;
        return empty;
    }

    gamma = 5. / 3.;

	//int mass;
    //cout << "Enter power of ten of mass of galaxy (9 for 10^9): ";
    //cin >> mass;
    m = pow(10, mass) * 1.9884 * pow(10, 33);

    int mass_halo;
    //cout << "Enter power of ten of halo mass: ";
    //cin >> mass_halo;
    mass_halo = 2;
    m_h = gsl_pow_int(10, mass_halo) * 1.9884 * gsl_pow_int(10, 33);

    //cout << "Enter characteristic halo length in kiloparsecs: ";
    //cin >> a;
    a = 5;
    a *= 3.0857*gsl_pow_int(10, 21);

    //cout << "Enter radius of mass and energy injection in parsecs: ";
    //cin >> rad;
    rad = 200;
    rad *= 3.0857*gsl_pow_int(10, 18);
	

    //cout << "Enter velocity at critical radius: ";
    //cin >> uc;
    double ucInput = uc;
	uc *= sqrt(G * m / rad);

    //cout << "Enter Magnetic Field in uG at 200pc: ";
    //cin >> B1;
    B1 *= gsl_pow_int(10,-6);

    //cout << "Wind shocks? (0 = No; 1 = Yes, without B field; 2 = Yes, WITH B field)";
    //cin >> shock;

	cout << "\n"; 
	
    vector<vector<double> > vec = with_energy_scaled_radiative(alpha, beta,
            SFR, gamma, m, rad, m_h, a, uc, shock, B1, P_IGM);
	
	vector<double> shockData3;
	bool tooSmall = false;
	bool emptyVec = false;
    ofstream file;
    file.open("data");
    //write numbers in scientific notation
    file << scientific;
	
	if(vec.size() < 4)
	{
		tooSmall = true;
	}
	if(!tooSmall && (vec[0].empty() || vec[1].empty() || vec[2].empty() || vec[3].empty()))
	{
		emptyVec = true;
	}
	if(!tooSmall && !emptyVec)
	{
		for (unsigned int i = 0; i < vec[0].size(); i++)
		{	
			for (unsigned int j = 0; j < 6; j++)
			{
				if (j == 0)
				{ // r
					file << vec[j][i];
					file << " ";
				}
				else if (j == 1)
				{ // u
					file << vec[j][i];
					file << " ";
				}
				else if (j == 2)
				{ // cs
					file << vec[j][i];
					file << " ";
				}
				else if (j == 3)
				{ // rho
					file << vec[j][i];
					file << " ";
				}
				else if (j == 4)
				{ // rho*u^2
					file << vec[3][i]*gsl_pow_2(vec[1][i]);
					file << " ";
				}	
				else if (j == 5)
				{ // temperature
					file << M_MASS*gsl_pow_2(vec[2][i])/(gamma*KB);
					file << " ";
				}
			}
			file << "\n";
		}
		file.close();
		
		//creating a vector to be returned so that a file can be created keeping track of all
		// of the different values
		vector<double> shockData1 = {alpha, beta, SFR, (double) mass, uc, B1,(double) shock, 0,0,0,0,0,0,0};
		vector<double> shockData2 = complete_data(shockData1);
		
		//Adding the central temperature to the data vector
		double centTemp = M_MASS*gsl_pow_2(vec[2][0])/(gamma*KB);
		shockData3 = add_Temp(shockData2, centTemp);
		
		cout << "ucInput: " << ucInput << "\n";
		
		//Add the x-ray luminosity to the returning vector
		vector<double> xRayLuminosity = xRayLum(ucInput, uc);
		shockData3.push_back(xRayLuminosity[0]);
	}
	else if(tooSmall)
	{
		cout << "ERROR: Data vector has size = " << vec.size() << ", Must have size = 4\n";
	}
	else if(emptyVec)
	{
		cout << "ERROR: One of the vectors is empty\n";
	}
	else{
		cout << "Uncaught Exception\n";
	}
	cout<<"END OF RUN\n";
	
    return shockData3;
}
