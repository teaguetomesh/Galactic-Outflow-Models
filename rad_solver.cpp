#include <stdio.h>
#include "gsl/gsl_math.h"
#include <iostream>
#include <gsl/gsl_poly.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_errno.h>
#include <math.h>

//gravitational constant
const double G = 6.6726e-8;
//boltz constant
const double KB = 1.3807e-16;
//mean mass per particle
const double M_MASS = 1.021e-24;

//structure used for parameters
struct parameters {double u; double gamma; double ksi; double me; double re;
    double mh; double a; double q0;};

double q(double r, double q0, double re)
{
	return q0 * (1. - gsl_pow_2(r) / gsl_pow_2(re));
}

double qavg(double r, double q0, double re)
{
	return q0 * (1 - 3. / 5. * gsl_pow_2(r) / gsl_pow_2(re));
}

double dq(double r, double q0, double re)
{
    return -2 * q0 * r / gsl_pow_2(re);
}

double dqavg(double r, double q0, double re)
{
    return -6 * q0 * r / (5 * gsl_pow_2(re));
}

//F is the function being solved for
double F(double r, void * p)
{
    //setup parameters
    struct parameters * params = (struct parameters *)p;
    double u = (params->u);
    double gamma = (params->gamma);
    double ksi = (params->ksi);
    double me = (params->me);
    double re = (params->re);
    double mh = (params->mh);
    double a = (params->a);
    double q0 = (params->q0);

    double qc = q(r, q0, re);
    double qcavg = qavg(r, q0, re);
    double dqc = dq(r, q0, re);
    double dqcavg = dqavg(r, q0, re);

    double dphi = G * mh / gsl_pow_2(r + a) + G * me * r / gsl_pow_3(re);
    double dphi2 = -2 * G * mh / gsl_pow_3(r + a) + G * me / gsl_pow_3(re);

    //setting up cooling function, Lambda
    double T = M_MASS * u * u / (gamma * KB);
    //double T = M_MASS * u / (gamma * KB) * G * me / re;
    double theta = log10(T / (2e5));
    //double theta = M_MASS * u * u * G * me / (2e5) * gamma * KB * re;
    double bigTheta = 0.4 * theta - 3 + 6.2 / ((exp(1.5 * theta + 0.08))
            + exp(-1 * (theta + 0.08)));
    double lambda0 = 1.5e-21;
    double lambda = lambda0 * pow(10, bigTheta);  


    double d = 3 * gamma * (gamma - 1) * ksi * qc / (qcavg * r)
        + 3 * (gamma - 1) * gsl_pow_3(u) / (qcavg * r) * (-2 * qcavg
        / (3 * u) + qc / u)
        - gamma * (gamma - 1) * qcavg * r * lambda / (3 * u * u * M_MASS * M_MASS);
    double d1 = gamma + 1;
    double d2 = -d / u;
    double n1 = -2 * (gamma - 1) * u / r - 6 * qc * u / (qcavg * r) + 3 * qc
        * (gamma - 1) * u / (qcavg * r) - 2 * (gamma - 1) * qcavg * r * lambda
        / (3 * M_MASS * M_MASS * u * u * u);
    double n2 = 2 * d / r - 2 * u * u / (r * r) - dphi2 - 3 * (gamma - 1) * ksi
        * dqc / (qcavg * r) + 3 * (gamma - 1) * ksi * qc * dqcavg / (qcavg
        * qcavg * r) + 3 * (gamma - 1) * ksi * qc / (qcavg * r * r)
        - 6 * u * u * dqc / (qcavg * r) - 3 * qc * d / (qcavg * r) + 6 * qc * u
        * u * dqcavg / (qcavg * qcavg * r) + 6 * qc * u * u / (qcavg * r * r)
        + (gamma - 1) * r * lambda  * dqcavg / (3 * M_MASS * M_MASS * u * u)
        + (gamma - 1) * qcavg * lambda / (3 * M_MASS * M_MASS * u * u);
    double du = (n1 - d2 + sqrt(gsl_pow_2(d2 - n1) + 4 * d1 * n2)) / (2 * d1);

    double dcs2 = 3 * gamma * (gamma - 1) * ksi * qc / (qcavg * r)
        + 3 * (gamma - 1) * gsl_pow_3(u) / (qcavg * r) * (-2 * qcavg
        / (3 * u) - qcavg * r * du / (3 * gsl_pow_2(u)) + qc / u)
        - gamma * (gamma - 1) * qcavg * r * lambda / (3 * u * u * M_MASS * M_MASS);

        
    //return function
    return qcavg * r * (-dcs2 / gsl_pow_2(u) + 2 * du / u) * du / 3 + 2
        * u * dqc + 2 * qc * du + qc * u * (dcs2 / gsl_pow_2(u) - 2 * du / u)
        + r * dqcavg * dphi / (3 * u) + qcavg * dphi / (3 * u) - qcavg * r
        * du * dphi / (3 * gsl_pow_2(u)) + qcavg * r * dphi2 / (3 * u) - 2
        * qcavg * dcs2 / (3 * u) - 2 * u * dqcavg / 3 + 2 * qcavg * du / 3
        + (gamma - 1) * ksi * dqc / u - (gamma - 1) * ksi * qc * du
        / gsl_pow_2(u) - (gamma - 1) * 2 * qcavg * r * r * lambda * dqcavg
        / (9 * M_MASS * M_MASS * u * u * u) - (gamma - 1) * 2 * qcavg * qcavg
        * r * lambda / (9 * M_MASS * M_MASS * u * u * u) + (gamma - 1) * qcavg
        * qcavg * r * r * lambda * du / (3 * M_MASS * M_MASS * u * u * u * u);
}



double find_crit_rad(double u, double gamma, double ksi, double me,
        double re, double mh, double a, double q0)
{
    //status checks if we are done or an error occurred
    int status;
    //max_iter specifies the max number of iterations
    int iter = 0, max_iter = 100;
    //declaring pointers for the root solver
    const gsl_root_fsolver_type *T;
    gsl_root_fsolver *s;

    double r = 0;
    //lower and upper bounds for r
    double r_lo = re * 0.5, r_hi = re;

    //turn off default error handling
    gsl_error_handler_t* handler = gsl_set_error_handler_off();
    //declare F a gsl function and with specified parameters
    gsl_function Function;
    struct parameters params = {u, gamma, ksi, me, re, mh, a, q0};
    Function.function = &F;
    Function.params = &params;

    //use brent root solver
    T = gsl_root_fsolver_brent;
    s = gsl_root_fsolver_alloc(T);
    //setup solver with type and bounds
    status = gsl_root_fsolver_set(s, &Function, r_lo, r_hi);
    if (status != GSL_SUCCESS)
        {
            gsl_root_fsolver_free(s);
            return -1;
        }

    //do successive iterations of root solving until within error
    //or max number of iterations is reached
    do
    {
        iter++;
        //iterate and get values of r, upper, and lower bounds
        status = gsl_root_fsolver_iterate(s);
        r = gsl_root_fsolver_root(s);
        r_lo = gsl_root_fsolver_x_lower(s);
        r_hi = gsl_root_fsolver_x_upper(s);
        //test if upper and lower bounds are within absolute error 0
        //and relative error 0.000001
        status = gsl_root_test_interval(r_lo, r_hi, 0, 0.000001);
    }
    while (status == GSL_CONTINUE && iter < max_iter);
    if (status != GSL_SUCCESS)
        {
            gsl_root_fsolver_free(s);
            return -1;
        }

    //release memory used by root solver
    gsl_root_fsolver_free(s);
    //restore error handler
    gsl_set_error_handler(handler);

    return r;
}
