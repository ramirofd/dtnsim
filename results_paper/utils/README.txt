This folder contains scripts that take as input files with a contact plan between 66 satellites of the Iridium constellation, KSAT ground stations, and HAPS that are located 20 km above the ground stations.

The following files are taken as input from the contactPlan folder:

contact_plan_7d_name_to_id_mapping.txt: contains the mapping between node names and their respective ids. 

contact_plan_7d_node-ids.txt: contains the contact plan between nodes (referenced by their ids)

The outputs are saved in the same contactPlan folder.

As an example, the script "main_5GS.py" generates a contact plan between 1 LEO and 5 Ground Stations.
Also, each Ground Station should be connected to a central node called MOC which is the final destination.

As another exaple, the script "main_1LEO_3HAP_3GS.py" generates a contact plan between 1 LEO and 3 HAPS.
Also, each HAPS connects through a permanent contact with their respective Ground Station. 
In addition, each Ground Station should be connected to a central node called MOC which is the final destination.
The contacts between HAPS and GS need to be added manually or modifying the scripts.


