#include <stdio.h>
#include <math.h>
#include <gsl/gsl_errno.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_odeiv2.h>
#include "gsl/gsl_math.h"
#include "gsl/gsl_poly.h"
#include "rad_solver.h"
#include <iostream>
#include <list>
#include <vector>
#include "store_data.h"
//#include <ctime>
using namespace std;

//gravitational constant
const double G = 6.6726e-8;
//Boltzmann's constant
const double KB = 1.3807e-16;
//distance away from critical point to start integration
const double DR = 0.00001e20;
//mean mass per particle
const double M_MASS = 1.021e-24;
//200pc
const double RAD = 6.171e20;

//structure used for parameters
struct parameters {double gamma;
    double ksi; double M; double rad; double q0; double a; double m_h;};

///////////////////////////////////
//For the region between r0 and R
//Sets up the differential equations for velocity and sound speed
int func (double r, const double y[], double f[], void *p)
{

    parameters * params = (parameters *)p;

    double gamma = (params->gamma);
    double ksi = (params->ksi);
    double M = (params->M);
    double rad = (params->rad);
    double q0 = (params->q0);
    double a = (params->a);
    double m_h = (params->m_h);

    //setting up cooling function, Lambda
    //double T = M_MASS * y[1] / (gamma * KB) * G * M / rad;
    double T = M_MASS * y[1] / (gamma * KB);
    double theta = log10(T / (2e5));
    double bigTheta = 0.4 * theta - 3 + 6.2 / ((exp(1.5 * theta + 0.08))
            + exp(-1 * (theta + 0.08)));
    double lambda0 = 1.5e-21;
    double lambda = lambda0 * pow(10, bigTheta);  

    double dphi = G * m_h / gsl_pow_2(r + a) + G * M * r / gsl_pow_3(rad);
    double qc = q(r, q0, rad);
    double qcavg = qavg(r, q0, rad);

    //f[0] is du/dr
    f[0] = (-qc * y[0] * (1 + y[1] / gsl_pow_2(y[0])) - qcavg
         * r * dphi / (3 * y[0]) + 2 * y[1] * qcavg / (3 * y[0])
         - (gamma - 1) * ksi * qc / y[0]) / (qcavg * r
         * (1 - y[1] / gsl_pow_2(y[0])) / 3) + (gamma - 1) * qcavg * r
         * lambda / (3 * M_MASS * M_MASS * gsl_pow_3(y[0]) * (1 - y[1]
         / (y[0] * y[0])));
    
    //f[1] is dcs^2/dr
    f[1] = 3 * gamma * (gamma - 1) * ksi * qc / (qcavg * r) + 3
         * (gamma - 1) * y[1] * y[0] * (-2 * qcavg
         / (3 * y[0]) - qcavg * r * f[0] / (3 * y[0] * y[0]) + qc
         / y[0]) / (qcavg * r) - gamma * (gamma - 1) * qcavg * r
         * lambda / (3 * y[0] * y[0] * M_MASS * M_MASS);

    return GSL_SUCCESS;
}




///////////////////////////////////
//For r > R
//Sets up the differential equations for velocity and sound speed
int func2 (double r, const double y[], double f[], void *p)
{
    parameters * params = (parameters *)p;

    double gamma = (params->gamma);
    double M = (params->M);
    double q0 = (params->q0);
    double a = (params->a);
    double m_h = (params->m_h);

    //setting up cooling function, Lambda
    //double T = M_MASS * y[1] / (gamma * KB) * G * M / rad;
    double T = M_MASS * y[1] / (gamma * KB);
    double theta = log10(T / (2e5));
    double bigTheta = 0.4 * theta - 3 + 6.2 / ((exp(1.5 * theta + 0.08))
            + exp(-1 * (theta + 0.08)));
    double lambda0 = 1.5e-21;
    double lambda = lambda0 * pow(10, bigTheta);  
    //need to look at mass

    double rho = 2 * q0 / (15 * r * r * y[0]);

    double dphi = G * m_h / gsl_pow_2(r + a) + G * M / gsl_pow_2(r);

    //f[0] is du/dr
    f[0] = (2 * y[1] * y[0] / r - y[0] * dphi) / (y[0] * y[0] - y[1])
        + (gamma - 1) * rho * lambda / (M_MASS * M_MASS * y[0] * y[0]);
    
    //f[1] is dcs^2/dr
    f[1] = (gamma - 1) * y[1] * (-2 * rho / r - rho * f[0] / y[0]) / rho
        - gamma * (gamma - 1) * rho * lambda / (y[0] * M_MASS * M_MASS);

    return GSL_SUCCESS;
}


//alpha = energy factor
//beta = mass-loading factor
//SFR = star formation rate
//gamma = polytropic index
//m = mass of galaxy
//m_h = mass of halo
//a = characteristic halo length scale
//rad = end of energy and mass injection
//uc = speed at critical radius
vector<vector<double> > with_energy_scaled_radiative (double alpha,
        double beta, double SFR, double gamma, double m, double rad, double m_h,
        double a, double uc, int shock, double B_init, double P_IGM)
{
    //start clock for timing
    //clock_t start;
    //double duration;
    //start = clock();
	
	//Boolean to keep track of whether or not a shock forms
	bool wildShock = false;
	//Other variables to help keep track of intermediate values
	//Needed at the end of this function to keep track of data
	double compRatio1, compRatio2, compRatio3 = 0;
	double Bfield = 0;
	double shockPos = 0;

    //beginning radius
    double r0 = 5 * 3.086e18;

    //mass loading per volume factor
    double q0 = beta * SFR * (6.30529e25)
        / (8. / 15. * M_PI * gsl_pow_3(rad));

    //need to generalize this for different gravities
    //only for 10^9 solar mass galaxies
    double ksi = alpha * 5.032e15;
	double rc = find_crit_rad(uc, gamma, ksi, m, rad, m_h, a, q0);
	if (rc < 0)
    {
		cout<<"ERROR: Critical Radius = " << rc << "\n";
        list<double> rlist;
        list<double> u;
        list<double> cs;
        rlist.push_front(0.);
        cs.push_front(0.);
        u.push_front(0.);
        vector<vector<double> > ret {{make_move_iterator(begin(rlist)),
            make_move_iterator(end(rlist))}, {make_move_iterator(begin(u)),
            make_move_iterator(end(u))}, {make_move_iterator(begin(cs)),
            make_move_iterator(end(cs))} };
		//cout<<"rlist size: " <<rlist.size()<<"\n";
		//cout<<"u size: " << u.size() << "\n";
		//cout<<"cs size: " << cs.size() << "\n";
		//cout<< "ret size: " << ret.size() << "\n";
        return ret;
    }
	cout << "Critical Radius: " << rc << "\t";
    cout << "uc: " << uc << "\n";

    parameters params = {gamma, ksi, m, rad, q0, a, m_h};	  

    gsl_odeiv2_system sys = {func, NULL, 2, &params};

    gsl_odeiv2_driver * d = 
        gsl_odeiv2_driver_alloc_y_new (&sys, gsl_odeiv2_step_rkf45,
		    -0.0000001e20, 1e-6, 0.0);
    double r = rc - DR;
    double r1 = r;
    double y[2] = { uc * 0.9999, gsl_pow_2(uc) };

    //boolean to check if integration failed
    bool failed = false;

    //set up lists for r, u, and cs
    list<double> rlist;
    list<double> u;
    list<double> cs;
    list<double> rholist;

    //number of points between r0 and rc
    int len1 = 100;

    //integrate inwards from the critical radius, r1, to r0 where r ~ 0
    //fills 0-99 in lists
    for (int i = len1 - 1; i >= 0; i--)
    {
        double ri = r0 + (r1 - r0) * i / len1;
        //driver goes from r to ri
        int status = gsl_odeiv2_driver_apply (d, &r, ri, y);

        if (status != GSL_SUCCESS)
        {
            printf ("error in 1, return value=%d\n", status);
            u.push_back(0.);
            cs.push_back(0.);
            rlist.push_back(2 * rad);
            failed = true;
            break;
        }

        u.push_front(y[0]);
        cs.push_front(sqrt(y[1]));
        rlist.push_front(ri);
        rholist.push_front(qavg(ri,q0,rad)*ri/(3*y[0]));
    }
  

    d = gsl_odeiv2_driver_alloc_y_new (&sys, gsl_odeiv2_step_rkf45,
        0.0000001e20, 1e-6, 0.0);

    r = rc + DR;
    r0 = r;
    r1 = rad;
    //starting point for integration
    y[0] = uc * 1.0001;
    y[1] = gsl_pow_2(uc);

    //number of points between rc and R
    int len2 = 20; 

    //integrate outwards from the critical radius to R
    //i.e. to 1 in scaled units. Fills 100-109 in lists
    if (failed)
    {
        len2 = 0;
    }
    for (int i = 1; i <= len2; i++)
    {
        double ri = r0 + (r1 - r0) * i / len2;
        int status = gsl_odeiv2_driver_apply (d, &r, ri, y);

        if (status != GSL_SUCCESS)
        {
            printf ("error in 2, return value=%d\n", status);
            u.push_back(0.);
            cs.push_back(0.);
            rlist.push_back(2 * rad);
            failed = true;
            break;
        }

        u.push_back(y[0]);
        cs.push_back(sqrt(y[1]));
        rlist.push_back(ri);
        rholist.push_back(qavg(ri,q0,rad)*ri/(3*y[0]));
    }


    // integrate from r = R to some endpoint
    double endPoint = 1000 * rad;  

    sys = {func2, NULL, 2, &params};
    d = gsl_odeiv2_driver_alloc_y_new (&sys, gsl_odeiv2_step_rkf45,
        0.0000001e20, 1e-6, 0.0);

	r = rad + DR;
    r0 = r;
    r1 = endPoint;
    //starting point for integration
    y[0] = u.back();
    y[1] = gsl_pow_2(cs.back()); 

    //number of points between R and endPoint
    int len3 = 9500;

    //integrate outwards from R to endPoint
    //i.e. to 1 in scaled units. Fills 110-149 in lists
	
    if (failed)
    {
        len3 = 0;
    }
    for (int i = 1; i <= len3; i++)
    {
        double ri = r0 + i * (r1 - r0) / len3;
        int status = gsl_odeiv2_driver_apply (d, &r, ri, y);

        if (status != GSL_SUCCESS)
        {
            printf ("error in 3, return value=%d\n", status);
            u.push_back(0.);
            cs.push_back(0.);
            rlist.push_back(ri);
            break;
        }
        double rho1 = rholist.back();
        double u1 = u.back();
        double Mach = u.back() / cs.back();
        double cs1 = cs.back();

        u.push_back(y[0]);
        cs.push_back(sqrt(y[1]));
        rlist.push_back(ri);
        rholist.push_back(qavg(RAD,q0,rad) * RAD * RAD * RAD /(3*gsl_pow_2(ri)*y[0]));

        double ratio;
        //double B2;
	
	double B1;
        //assume B falls off as 1/r:
        B1 = B_init*RAD/ri;
//	cout << B1 << "\n"; 
	
	//Define the pre-shock and post-shock total pressures as the sum of ram pressure, gas pressure, mag pressure
	double totalPressure_pre;
	double totalPressure_post;
	totalPressure_pre = rho1*gsl_pow_2(u1) + rho1*gsl_pow_2(cs1)/gamma + gsl_pow_2(B1)/(8*M_PI);
	totalPressure_post = (rholist.back())*gsl_pow_2(u.back()) + (rholist.back())*gsl_pow_2(cs.back())/gamma + gsl_pow_2(B1)/(8*M_PI);

        if ((totalPressure_pre > P_IGM) && (totalPressure_post < P_IGM) && (Mach > 1.0))
        { 
			wildShock = true;
            printf("A wild shock appears! \n");
            cout << "B field strength at shock: " << B1 << " G \n";
			//Keeping track of intermediate values
			Bfield = B1;
            if (shock == 1)
            {
                //insert Rankine-Hugoniot jump conditions
		        cout << "Shock position: " << ri/(3.0857e18) << " pc \n";
				
				//Keeping track of intermediate values
				shockPos = ri/(3.0857e18);

                rholist.back() = gsl_pow_int(((gamma-1)/(gamma+1) + 2*y[1]/((gamma+1)*gsl_pow_2(y[0]))),-1)*rho1;
                u.back() = ((gamma-1)/(gamma+1)+2*y[1]/((gamma+1)*gsl_pow_2(y[0])))*u1;
                //PR = (2*gamma/(gamma+1)*gsl_pow_2(u[len1+len2+i-2]/cs[len1+len2+i-2]) - (gamma-1)/(gamma+1))*rhovec[len1+len2+i-2]*y[1];
                cs.back() =  sqrt((2*gamma*gsl_pow_2(Mach) - (gamma-1))*(gamma-1+2/gsl_pow_2(Mach))/(gsl_pow_2(gamma+1)))*cs1;
		        cout << "Compression ratio: " << u1/u.back() << "\n";
				//Keeping track of intermediate values
				compRatio1 = u1;
				compRatio2 = u.back();
                /*
                cout << "u: " << u.back() / sqrt(G * m / rad) << "\n";
                cout << "cs: " << cs.back() / sqrt (G * m / rad) << "\n";
                */
		d = gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rkf45, 0.0000001e20, 1e-6, 0.0);
            }
            else if (shock == 2)
            { //magnetized shock
                double x0, x1, x2;
                gsl_poly_solve_cubic((u1/(gsl_pow_2(Mach)*(gamma-1)) + u1*gamma/(gamma-1) + gsl_pow_2(B1)*gamma/(8*M_PI*rho1*u1*(gamma-1)))/(1./2.-gamma/(gamma-1)), -(gsl_pow_2(B1)/(4*M_PI*rho1) + gsl_pow_2(u1)*(1./2. + 1/(gsl_pow_2(Mach)*(gamma-1))))/(1./2. - gamma/(gamma-1)), -(gsl_pow_2(B1)/(4*M_PI*rho1)*u1*(gamma/(2*(gamma-1))-1))/(1./2. - gamma/(gamma-1)),&x0,&x1,&x2);
                /*
                cout << u1 << "\n";
                printf("A wild shock appears! \n");
                cout << x0 << "\n";
                cout << x1 << "\n";
                cout << x2 << "\n";

		        */
		
	        	cout << "Shock position: " << ri/(3.0857e18) << "pc \n";
				
				//Keeping track of intermediate values
				shockPos = ri/(3.0857e18);
                
				ratio = x1/u1;
                if (x1 > u1)
                {
                    cout << "Compression ratio < 1; Program stops" << "\n";
                }
                cout << "Compression Ratio: " << 1./ratio << "\n";
				
				//Keeping track of intermediate values
				compRatio3 = ratio;
				
                u.back() = ratio*u1; // u2
                rholist.back() = rho1/ratio; //rho 2
                //B2 = B1/ratio;
                cs.back() = sqrt((1+gamma*gsl_pow_2(Mach*B1/u1)/(8*M_PI*rho1)*(1-gsl_pow_2(ratio)) + gamma*gsl_pow_2(Mach)*(1-ratio))*ratio)*cs1;
		d = gsl_odeiv2_driver_alloc_y_new(&sys, gsl_odeiv2_step_rkf45, 0.0000001e20, 1e-6, 0.0);
            }
        }
        y[0] = u.back();
        y[1] = gsl_pow_2(cs.back());
        /*
        cout << "y[0]: " << y[0] / sqrt(G * m / rad) << "\n";
        cout << "y[1]: " << sqrt(y[1]) / sqrt(G * m / rad) << "\n";
        */
    }

  
    gsl_odeiv2_driver_free (d);

    //chop off anything that isn't a number
    //nan comparison is always false
    list<double>::iterator uit = u.begin();
    list<double>::iterator csit = cs.begin();
    list<double>::iterator rit = rlist.begin();
    list<double>::iterator rhoit = rholist.begin();
    while (rit != rlist.end())
    {
        if ((*rit != *rit) || (*uit != *uit) || (*csit != *csit) || (*rhoit != *rhoit))
        {
            uit = u.erase(uit);
            csit = cs.erase(csit);
            rit = rlist.erase(rit);
            rhoit = rholist.erase(rhoit);
            //cout << "nan encountered\n";
        }
        else
        {
            ++rit;
            ++uit;
            ++csit;
            ++rhoit;
        }
    }
    

    vector<vector<double> > ret {{make_move_iterator(begin(rlist)),
            make_move_iterator(end(rlist))}, {make_move_iterator(begin(u)),
            make_move_iterator(end(u))}, {make_move_iterator(begin(cs)),
            make_move_iterator(end(cs))}, {make_move_iterator(begin(rholist)),
            make_move_iterator(end(rholist))} };
    /*
    cout << "r = " << ret[0].front() << "\n";
    cout << "u = " << ret[1].front() << "\n";
    cout << "cs = " << ret[2].front() << "\n";
    cout << "q = " << q(ret[0].front(), q0, rad) << "\n";
    cout << "qavg = " << qavg(ret[0].front(), q0, rad) << "\n";
    cout << "ksi = " << ksi << "\n";
    cout << "m = " << M_MASS << "\n";
    double T = M_MASS * ret[2].front() * ret[2].front() / (gamma * KB);
    double theta = log10(T / (2e5));
    double bigTheta = 0.4 * theta - 3 + 6.2 / ((exp(1.5 * theta + 0.08))
            + exp(-1 * (theta + 0.08)));
    double lambda0 = 1.5e-21;
    double lambda = lambda0 * pow(10, bigTheta);
    cout << "lambda = " << lambda << "\n";
    cout << "Calculated T = " << T << "\n";
    */
    //retrieve and print time
    //duration = (clock() - start) / (double)CLOCKS_PER_SEC;
    //std::cout << "Running time: " << duration << '\n';

	//Sending out the calculated values so that a file can be made
	//keeping track of all of their values
	double shockPresent = 0;
	double compRatio = 0;
	if(wildShock)
	{
		shockPresent = 1;
	}
	if(shock == 1 && shockPresent == 1)
	{
		compRatio = compRatio1/compRatio2;
	}
	else if(shock == 2 && shockPresent == 1)
	{
		compRatio = 1./compRatio3;
	}
	
	//function found in store_data.cpp
	store_data(rc, uc, shockPresent, Bfield, shockPos, compRatio);
	
    return ret;
}
