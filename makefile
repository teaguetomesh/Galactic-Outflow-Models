rad_solver: rad_solver.cpp
	g++ -std=c++11 -Wall -c -I/opt/local/include/ run_model_many.cpp rad_solver.cpp with_energy_scaled_radiative.cpp model_without_prompts.cpp store_data.cpp xRayLum.cpp model_without_prompts_v2.cpp
	g++ -o  simulate run_model_many.o rad_solver.o with_energy_scaled_radiative.o model_without_prompts.o store_data.o xRayLum.o model_without_prompts_v2.o -L/opt/local/lib/ -lgsl -lgslcblas -lm
