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

vector<double> model_without_prompts_v2(double alpha, double beta, double SFR, double uc,
									 double B1, int shock, double mass, double rad)
{
	const double P_IGM = gsl_pow_int(10,-14);
    const double G = 6.6726 * gsl_pow_int(10, -8);
    const double KB = 1.3807 * gsl_pow_int(10, -16); 
    const double M_MASS = 1.021 * gsl_pow_int(10, -24);
    double gamma, m, m_h, a;
  
    int in;
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

    m = gsl_pow_int(10, mass) * 1.9884 * gsl_pow_int(10, 33);

    int mass_halo;
    mass_halo = 2;
    m_h = gsl_pow_int(10, mass_halo) * 1.9884 * gsl_pow_int(10, 33);

    //characteristic halo length in kiloparsecs;
    a = 5;
    a *= 3.0857*gsl_pow_int(10, 21);

    //radius of mass and energy injection in parsecs;
    rad = 200;
    rad *= 3.0857*gsl_pow_int(10, 18);
	

    //velocity at critical radius;
    double ucInput = uc;
	uc *= sqrt(G * m / rad);

    //Magnetic Field in uG at 200pc;
    B1 *= gsl_pow_int(10,-6);

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
		return {0};
	}
	else if(vec[0].empty() || vec[1].empty() || vec[2].empty() || vec[3].empty())
	{
		emptyVec = true;
		return {0};
	}
	
	//Use this if statement to stop the code if an error is reached
	if(vec[0][0] == 0 && vec[1][0] == 0 && vec[2][0] == 0 && vec[3][0] == 0)
	{
		return 	{0};
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
	}
	//creating a vector to be returned so that a file can be created keeping track of all
	// of the different values
	vector<double> shockData1 = {alpha, beta, SFR, (double) mass, uc, B1,(double) shock, 0,0,0,0,0,0,0};
	vector<double> shockData2 = complete_data(shockData1);
		
	//Adding the central temperature to the data vector
	double centTemp = M_MASS*gsl_pow_2(vec[2][0])/(gamma*KB);
	shockData3 = add_Temp(shockData2, centTemp);
		
	double Mach_pre1, Mach_post1, shockRad;
	for (unsigned int k = 1; k < vec[0].size()-1; k++) 
	{
		// find shock and calculate shock quantities
		Mach_pre1 = vec[1][k]/vec[2][k];
		Mach_post1 = vec[1][k+1]/vec[2][k+1];
			
		if ((Mach_pre1 > 1.0) && (Mach_post1 < 1.0)) 
		{
			shockRad = vec[0][k]; //radius of shock
		}	   
	}	
		
	//Add the x-ray luminosity to the returning vector
	vector<double> xRayLuminosity = xRayLum(ucInput, uc, rad, shockRad);
	shockData3.push_back(xRayLuminosity[0]);
		
	//Add more values to returning vector
	double Mach_pre, Mach_post;
	for (unsigned int k = 1; k < vec[0].size()-1; k++) 
	{
		// find shock and calculate shock quantities
		Mach_pre = vec[1][k]/vec[2][k];
		Mach_post = vec[1][k+1]/vec[2][k+1];
			
		if ((Mach_pre > 1.0) && (Mach_post < 1.0)) 
		{
			shockData3.push_back(vec[0][k]); //radius of shock
			shockData3.push_back(vec[1][k]/vec[2][k]); //mach number
			shockData3.push_back(vec[1][k]); //asymptotic velocity
			//tempAsym = M_MASS*gsl_pow_2(vec[2][k])/(gamma*KB); // temp just before shock
			shockData3.push_back(vec[3][k]); //density at shock
			shockData3.push_back(M_MASS*gsl_pow_2(vec[2][k+1])/(gamma*KB)); //temp just after shock
			//B_shock = B_r; // magnetic field strength at shock
		}
				   
	}

	cout<<"END OF RUN\n";
	
	return shockData3;
}