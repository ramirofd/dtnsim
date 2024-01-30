The simulation_creator file has the following functions
- Delete each simulation file at the beginning (line 62)
- The possibility to choose how many LEOS, GS and HAGS to use (line 87)
- Create all the .ini AND script.sh to run all the repetitions of a simulation.
- The creation of a run.sh to execute all the scripts.sh (in /HAGS_Analysis)

Everything is fully automated : the files are directly in the right place.

To run the simulations :
- run simulation_creator.py
- run run.sh (I need to split it because it crashed my computer :( )
- wait :)
- run plot_all.py in /utils
- run plot_all.py in /results_paper
- View the results 