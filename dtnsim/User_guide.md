# DtnSim User Guide
This document provides help with Omnet++ in general and DtnSim. Its main goal is to help new users with the use of DtnSim.

# Omnet++
This section contains tips about Omnet++ in general.

+ Omnet++ doesn't not support well fractional scaling on linux. To avoid issues when using it, don't restart omnet++ when the pop-up shows, but simply put Omnet++ on your main screen defined in linux settings.

+ It's not necessary to put the environment variables in your bashrc/zprofile file. If Omnet++ is installed, you can just go to its directory and type :
```
source setenv
omnetpp
```
This will launch Omnet++.

+ At the top right of the interface, there are 3 buttons: Simulation, Team synchronising, and Debug. If the Run button does not appear in its right place, click on the Simulation button to return to the correct graphical interface.

+ Reinstalling Omnet++ can be a great solution. It's possible to activate multiprocessing during the compilation to make it faster (see the official install guide).

# DtnSim
This section contains tips and good practices about DtnSim.

+ The following characters cannot be in filenames in Windows. 
```
< (less than)
> (greater than)
: (colon)
" (double quote)
/ (forward slash)
\ (backslash)
| (vertical bar or pipe)
? (question mark)
* (asterisk)
```
So a file must not be named using one of these characters to avoid any issues with cloning the repository on Windows.

+ 

+ If something goes really wrong when using the simulator, delete all the file and clone the repository again.
```
source setenv
omnetpp
```
This will launch Omnetp++.

+ At the top right of the interface, there is 3 buttons : Simulation, Team synchronising and Debug. If the Run button does not appear at his right place, click on the Simulation button to go back to the right graphical interface.

+ Re-installing Omnet++ can be a great solution. It's possible to activate multiprocessing during the compilation to make it faster (see the official install guide).


# DtnSim
This section contains tips and good practises about DtnSim.

+ These following caractères connot be in filenames in Windows. So a file must not be named using one of these caracteres to avoid any issues with cloning the repository on windows.
```
< (less than)
> (greater than)
: (colon)
" (double quote)
/ (forward slash)
\ (backslash)
| (vertical bar or pipe)
? (question mark)
* (asterisk)
```

+ 

+ If something goes really wrong when using the simulator, delete all the files and clone the repository again.