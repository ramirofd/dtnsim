The simulation_creator.py file has the following functions : 
- Delete each simulation file at the beginning (line 62)
- The possibility to choose how many LEOS, GS and HAGS to use (line 87)
- Create all the .ini AND script.sh to run all the repetitions of a simulation.
- The creation of a run.sh to execute all the scripts.sh (in /HAGS_Analysis)

The data_processing.py file has the following functions: 
- Retrieve the data from the Omnetpp simulations
- Process this data to store it in a .json file 

The plot_processing.py file has the following functions:
- Automatically create all the plots for all the selected simulations.

Note : for each file, you must initialise number_of_LEOS_wanted, number_of_GS_wanted, number_of_HAGS_GS_wanted.

To run the simulations :
- run simulation_creator.py
- run runxLEO.sh
- wait :)
- run data_processing.py
- run plot_processing.py
- View the results in extension_results_xLEO/plots


Note : In total there are 21 HAGS/GS and 66 LEOs.