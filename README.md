# Transport Temperature Model

This repository contains the proposed model of the bachelor thesis "Thermal Modeling of Battery Systems on Transport Routes".  The program simulates the temperature during transports of lithium-ion batteries and systems in cargo carriers, e.g. shipping containers.

## Getting Started

<!---

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The thermal simulation is executed with the open source CFD software OpenFOAM. What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo
--->

## Running a transport simulation

A transport simulation can be executed in a folder that contains a **transport.json** file. This is the main input file and includes all informations about the start time of the transport, the transport route and the cargo. 

The simulation can be started with the simple command
```
ttm
```
If the current directory is not the directory where the simulation shall be executed, one can use the command
```
ttm --transport path_to_directory
```
The default configuration uses parallelisation with two local CPU cores. If desired, a custom core count can be set with the command
```
ttm --cpucores core_count
```
Additional commands are shown in the help 
```
ttm --help
```

### Results

After the simulation the postprocessing utility collects all results in the postProcessing directory. The results are saved as CSV files. Data from each simulated region, e.g. airInside or battery0_0, are saved in seperate files. 

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


<!---
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
--->