I used these files for my work on buckling on periodic structures.
You can probably use it to get an idea of the possibilities of coupling Matlab with Abaqus. 
Therefore, the files are not meant to explain in any way the calculation of buckling of periodic structures. 

The order of the programme is as follows:

First the Matlab file with MainBrutePois.m is called. This will call for the other Matlab files.
The matlab files will create the variables used in Abaqus. These variables are written to a text file in MakeVar.m.
Next Modelcalc.m will call Abaqus and runs the Python script files. 
The Python script files will first read the variables from the text file and create the model according to these variables.
After the simulation is done, Abaqus writes the interesting data to an output files (I create the output file myself, it is not a standard Abaqus output file).
Then Abaqus quites and Matlab will continue by reading the output text file from Abaqus.
