# Transport Temperature Model

This repository contains the proposed model of the bachelor thesis "Thermal Modeling of Battery Systems on Transport Routes".  The program simulates the temperature during transports of lithium-ion batteries and systems in cargo carriers, e.g. shipping containers.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites - OpenFOAM

The thermal simulation is executed with the open source CFD software OpenFOAM. The simulation case is compatible to OpenFOAM 7 v2006 , which must be installed on the system. An installation guide for debian/ubuntu systems can be found [here](https://develop.openfoam.com/Development/openfoam/-/wikis/precompiled/debian). For newer versions of OpenFOAM the template case has to be adapted.

### Installing
After cloning the repository, you can install the module with the included setup script. Run
```
python setup.py install --user
```
to install localy. 
If you want to install in develop mode run
```
python setup.py develop --user
```
In develop mode changes to the code will be reflected immediately in the behaviour of the program.

## Running a transport simulation

A transport simulation can be executed in a folder that contains a **transport.json** file. This is the main input file and includes all information about the start time of the transport, the transport route and the cargo. A full explanation of all possible inputs can be found in the documentation.

The simulation can be started with the simple command
```
ttm
```
If the current directory is not the directory where the simulation shall be executed, one can use the command
```
ttm --transport path_to_directory
```
The default configuration uses parallelisation with four local CPU cores. If desired, a custom core count can be set with the command
```
ttm --cpucores core_count
```
For additional commands run 
```
ttm --help
```

### Results

After the simulation the postprocessing utility collects all results in the postProcessing directory. The results are saved as CSV files. Data from each simulated region, e.g. airInside or battery0_0, is saved in a seperate file. 

 * transport
	 * case
	 *  plots
	 * postProcessing
		 * arrival
		 * probes
		 * temperature
			 * airInside.csv
			 * battery0_0.csv
			 * ...
		 * wallHeatFlux
		 * heattransfercoefficient.csv
		 * speed.csv
	 * transport.json
	 * weatherdata.csv

## Authors

* **Sammy Breen** - s.breen@tum.de