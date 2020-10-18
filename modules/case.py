from contextlib import redirect_stdout
import copy
import csv   
from datetime import datetime, timedelta
import glob
import json
from math import ceil
import os
import pytz
import re
import shutil
import sys

import geopy.distance
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector
from scipy.spatial.transform import Rotation
import tikzplotlib
from tzwhere import tzwhere

import modules.convection as convection
from modules.cargo import cargoDecoder
import modules.openfoam as openfoam
from modules.route import direction_crossover, add_seconds
from modules.transport import TransportDecoder

# For saving plots to file
matplotlib.use('Agg')

# Specific parameter values for different types of transports
TRANSPORTTYPES = {
    'container': {        
        'length': 6.0585,
        'width': 2.4390, 
        'height': 2.3855,
        'kappaLayers': 44,
        'thicknessLayers': 0.02
    },
    'carrier': {
        'length': 13.0005,
        'width': 2.4610, 
        'height': 2.5505,
        'kappaLayers': 0.5,
        'thicknessLayers': 0.01
    }
}

class Case(SolutionDirectory):
    def __init__(self, name, archive = None, paraviewLink = True):
        SolutionDirectory.__init__(self, name, archive = None, paraviewLink = True)
        
        if not os.path.exists(os.path.join(self.name,'logs')):
            os.makedirs(os.path.join(self.name,'logs'))

        #Add scripts and log folder to control simulation to cloneCase
        self.addToClone('Allrun.pre')
        self.addToClone('Run')
        self.addToClone('Reconstruct')
        self.addToClone('PostProcess')
        self.addToClone('ChangeDictionary')
        self.addToClone('ChangeDictionarySolid')
        self.addToClone('logs')

    def change_initial_temperature(self, temperature):
        # Convert to Kelvin
        temperature += 273.15
        print('Setting initial temperature for air and cargo to {} Kelvin'.format(temperature))
        changeDictionaryDict_airInside = ParsedParameterFile(
            os.path.join(self.systemDir(), "airInside", "changeDictionaryDict")
            )
        changeDictionaryDict_battery = ParsedParameterFile(
            os.path.join(self.systemDir(), "battery_template", "changeDictionaryDict")
            )

        changeDictionaryDict_airInside['T']['internalField'] = 'uniform {}'.format(temperature)
        changeDictionaryDict_battery['T']['internalField'] = 'uniform {}'.format(temperature)

        changeDictionaryDict_airInside.writeFile()
        changeDictionaryDict_battery.writeFile()

    def change_transporttype(self, transporttype):
        """Change transport specific parameters"""

        if transporttype not in TRANSPORTTYPES:
            raise ValueError("Case.change_dimensions(): transporttype must be one of %r." % TRANSPORTTYPES)

        transport = TRANSPORTTYPES[transporttype]
        
        blockMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "blockMeshDict"))
        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))
        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))

        # Minimal cellsize of blockMesh background mesh cells
        CELLSIZE = 0.32

        # Calculate dimensions for blockMesh 
        number_blocks_x = ceil(transport['length'] / CELLSIZE)
        number_blocks_y = ceil(transport['width'] / CELLSIZE)
        number_blocks_z = ceil(transport['height'] / CELLSIZE)
        # Write the geometry of the backgroundmesh to blockMeshDict
        blockMeshDict['length'] = number_blocks_x * CELLSIZE
        blockMeshDict['width'] = number_blocks_y * CELLSIZE / 2
        blockMeshDict['negWidth'] = - number_blocks_y * CELLSIZE / 2
        blockMeshDict['height'] = number_blocks_z * CELLSIZE
        # Write the number of blocks per dimension
        blockMeshDict['blocks'][2] = Vector(number_blocks_y, number_blocks_x, number_blocks_z)
        # Create geometry of carrier in snappyHexmeshDict
        snappyHexMeshDict['geometry']['carrier']['min'] = Vector(0.0005, -transport['width']/2, -0.0005)
        snappyHexMeshDict['geometry']['carrier']['max'] = Vector(transport['length'], transport['width']/2, transport['height'])
        # Change the thermal resistance of the wall of the carrier
        changeDictionaryDict['T']['boundaryField']['carrier']['kappaLayers'] = '( {} )'.format(transport['kappaLayers'])
        changeDictionaryDict['T']['boundaryField']['carrier']['thicknessLayers'] = '( {} )'.format(transport['thicknessLayers'])

        blockMeshDict.writeFile()
        changeDictionaryDict.writeFile()
        snappyHexMeshDict.writeFile()
    
    def load_cargo(self, cargo):
        """Loads the carrier with cargo. New regions for cargo 
        are added to snappyHexMeshDict and regionProperties"""
        # refinementLevel for cargo regions
        REFINEMENTSURFACELEVEL = [3,3]

        # Open files that need to be modified
        regionProperties = ParsedParameterFile(os.path.join(self.constantDir(),'regionProperties'))
        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))

        # Iteration over all cargo entries
        for i in range(len(cargo)):
            cargo_name = cargo[i].type.lower() + str(i)
            cargo[i].move_STL(self, cargo_name + '.stl')

            # Adding current cargo to the snappyHexMeshDict
            snappyHexMeshDict['geometry'].__setitem__(cargo_name + '.stl', {'type': 'triSurfaceMesh', 'name': cargo_name})
            snappyHexMeshDict['castellatedMeshControls']['refinementSurfaces'].__setitem__(cargo_name, {'level': REFINEMENTSURFACELEVEL})

            # Iteration over all individual battery regions in the cargo
            for j in range(len(cargo[i].battery_regions)):
                battery = cargo[i].battery_regions[j]
                battery.name = "battery" + str(i) + '_' + str(j)

                snappyHexMeshDict['castellatedMeshControls']['locationsInMesh'].append(
                    [Vector(battery.position[0], battery.position[1], battery.position[2]), battery.name]
                    )

                # Copy the battery template folders 
                shutil.copytree(os.path.join(self.systemDir(), "battery_template"), os.path.join(self.systemDir(), battery.name))
                shutil.copytree(os.path.join(self.constantDir(), "battery_template"), os.path.join(self.name, "constant", battery.name))
                shutil.copytree(os.path.join(self.name, "0.org", "battery_template"), os.path.join(self.name, "0.org", battery.name))
                # Write thermophysical properties to the region
                thermophysicalProperties = ParsedParameterFile(os.path.join(self.constantDir(), battery.name, 'thermophysicalProperties'))
                thermophysicalProperties['mixture']['thermodynamics']['Cp'] = battery.thermal_capacity()
                thermophysicalProperties['mixture']['equationOfState']['rho'] = battery.density()
                thermophysicalProperties.writeFile()

                # Write boundary conditions for battery region and airInside region
                changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), battery.name, 'changeDictionaryDict'))
                openfoam.region_coupling_solid_anisotrop['thicknessLayers'] = '( {} )'.format(battery.packaging_thickness())
                openfoam.region_coupling_solid_anisotrop['kappaLayers'] = '( {} )'.format(battery.thermal_conductivity_packaging)
                changeDictionaryDict['T']['boundaryField'][battery.name + '_to_airInside'] = openfoam.region_coupling_solid_anisotrop
                changeDictionaryDict.writeFile()

                changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), 'airInside', 'changeDictionaryDict'))
                openfoam.region_coupling_fluid['thicknessLayers'] = '( {} )'.format(battery.packaging_thickness())
                openfoam.region_coupling_fluid['kappaLayers'] = '( {} )'.format(battery.thermal_conductivity_packaging)
                changeDictionaryDict['T']['boundaryField']['airInside_to_'+ battery.name] = openfoam.region_coupling_fluid
                changeDictionaryDict.writeFile()

                #Names of the solid regions are in third entry of the list regions, adding batteries
                regionProperties['regions'][3].append(battery.name)

                self.create_function_objects(battery.name, controlDict)

        regionProperties.writeFile()
        snappyHexMeshDict.writeFile()
        controlDict.writeFile()

    def load_weatherdata(self):
        # Load weatherdata from csv file
        weatherdata_path = os.path.join(self.name, os.pardir, 'weatherdata.csv') 
        self.weatherdata = pd.read_csv(weatherdata_path, parse_dates = ['Date'], date_parser = pd.to_datetime)
        
    def create_mesh(self):
        os.system(os.path.join(self.name,"Allrun.pre"))
        self._move_logs()

        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))

        # Delete values that do not need to be changed anymore, so values for the last timestep are not overwritten 
        # when OpenFOAM function changeDict is executed
        del changeDictionaryDict['T']['internalField']
        del changeDictionaryDict['U']
        del changeDictionaryDict['p_rgh']
        del changeDictionaryDict['p']

        changeDictionaryDict.writeFile()

    def heattransfer_coefficient(self, T_U, u, region = 'airInside'):
        """Calculate heattransfer coefficient"""
        # Value for current time is saved in folder for last time
        times = self.getParallelTimes()

        # If times has only one entry, that means only 0 folder exists, 
        # thus average path temperature is initial temperature
        if len(times) == 1:
            airInside0T = ParsedParameterFile(os.path.join(self.name, '0', region, 'T'))
            T_W = re.findall(r"[-+]?\d*\.\d+|\d+", str(airInside0T['internalField']))
            T_W = float(T_W[0])
        # Else use average patch temperature
        else:
            time = times[-2]
            path_averageTemperature = os.path.join(
                self.name,'postProcessing',region,'wallTemperature_' + region, str(time),'surfaceFieldValue.dat'
                )    
            df_patch_temperature = pd.read_table(
                path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T']
                )

            # OpenFOAM sometimes changes naming of surfaceFieldValue file, make sure that dataframe reads the data
            if df_patch_temperature.empty:
                path_averageTemperature = os.path.join(
                    self.name,'postProcessing',region,'wallTemperature_' + region,
                    str(time),'surfaceFieldValue_' + str(time) + '.dat'
                )
                df_patch_temperature = pd.read_table(
                    path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T']
                    )
            T_W = df_patch_temperature['T'].iloc[-1]

        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))
        if u < 4:
            # Length for natural convection is z-axis value of geometry of carrier
            L = snappyHexMeshDict['geometry']['carrier']['max'][2]
            return convection.coeff_natural(L, T_W, T_U), T_W
        else:
            # Length for forced convection is x-axis value of geometry of carrier
            L = snappyHexMeshDict['geometry']['carrier']['max'][0]
            return convection.coeff_forced(L, u), T_W

    def run(self):
        """Execute the simulation"""
        self.load_weatherdata()
        
        path_solver_logfile = os.path.join(self.name,"log.chtMultiRegionFoam")

        # When solver restarts from other time than 0, remove solver logfile
        if os.path.exists(path_solver_logfile):
            os.remove(path_solver_logfile)

        # Open files that need to be modified
        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
        radiationProperties =  ParsedParameterFile(os.path.join(self.constantDir(), "airInside", "radiationProperties"))

        latesttime = float(self.getParallelTimes()[-1])
        transport_duration = self.weatherdata['Date'].iloc[-1] - self.weatherdata['Date'].iloc[0] 
        transport_duration = transport_duration.total_seconds()

        # Get index of current timestamp
        current_timestamp = self.weatherdata['Date'].iloc[0] + timedelta(seconds = latesttime)
        i = self.weatherdata['Date'].sub(current_timestamp).abs().idxmin()

        # Iterate over weatherdata
        while latesttime < transport_duration:
            # Read temperature and transform from Celsius to Kelvin
            temperature = self.weatherdata['T'].values[i] + 273.15

            current_timestamp = self.weatherdata['Date'].iloc[i]
            string_current_timestamp = current_timestamp.strftime('%Y-%m-%d_%H:%M:%S')

            # Update endTime of the simulation
            endTime_delta = self.weatherdata['Date'].values[i+1] - self.weatherdata['Date'].values[i]
            endTime_delta = endTime_delta / np.timedelta64(1, 's')
            controlDict['writeInterval'] = np.floor(endTime_delta)
            controlDict['endTime'] = latesttime + endTime_delta
            controlDict.writeFile()

            # Calculate travelspeed between waypoints
            coordinates = self.weatherdata[['Lat', 'Lon']].values[i]
            coordinates_next = self.weatherdata[['Lat', 'Lon']].values[i+1]
            distance = geopy.distance.distance(coordinates, coordinates_next).m
            travelspeed = distance / endTime_delta

            # #Upadate positon
            self._update_radiationProperties(
                radiationProperties, current_timestamp, coordinates, coordinates_next
                )

            # Print to console            
            print('Timestamp: {} (UTC)'.format(string_current_timestamp))
            print('Latitude: {0} Longitude: {1}'.format(coordinates[0], coordinates[1]))
            print('Temperature: {}'.format(temperature))
            print('Travelspeed: {}'.format(travelspeed))

            # Update the heattransfer coefficient 
            heattransfer_coefficient, T_W = self.heattransfer_coefficient(temperature, travelspeed)
            print('Recalculating heattransfer coefficient:')
            print('Heattransfer coeffcient: {0} with average wall temperature: {1}'.format(heattransfer_coefficient, T_W))

            # Write changes to changeDictionaryDict
            changeDictionaryDict['T']['boundaryField'] = {}
            changeDictionaryDict['T']['boundaryField']['carrier'] = {
                'h': heattransfer_coefficient,
                'Ta': temperature,
            }
            changeDictionaryDict['T']['boundaryField']['bottom'] = {
                'Ta': temperature
            }
            changeDictionaryDict.writeFile()
            
            #Write travelspeed and heattransfercoeffiecient to file
            self._save_data([latesttime, travelspeed], 'speed.csv')
            self._save_data([latesttime, heattransfer_coefficient], 'heattransfercoefficient.csv')

            # Execute solver
            self._move_logs()
            os.system(os.path.join(self.name,"ChangeDictionary"))
            os.system(os.path.join(self.name,"Run"))

            #File management of log files
            target = os.path.join(self.name,"log.chtMultiRegionFoam" + '_' + string_current_timestamp)
            shutil.move(path_solver_logfile, target)

            latesttime = float(self.getParallelTimes()[-1])
            i = i + 1

        print('Last timestep finished')
        self._move_logs()

    def _update_radiationProperties(self, radiationProperties, timestamp, coordinates, coordinates_next):
        startdate = self.weatherdata['Date'].iloc[0]
        # Get offset to UTC time
        localStandardMeridian = utcoffset(
            timestamp, self.weatherdata['Lat'].iloc[0], self.weatherdata['Lon'].iloc[0]
            )
        # Transform UTC time to local time
        startdate += timedelta(hours = localStandardMeridian)
        # Get time in decimal format
        starttime = startdate.time()
        starttime = starttime.hour + starttime.minute / 60 + starttime.second / 3600
        # Get startday as the number of the day in given year
        startday = startdate.timetuple().tm_yday
        # Calculate vector for east in grid coordinates
        direction = direction_crossover(coordinates, coordinates_next)
        # latitude matches y, longitude matches x
        x_axis = np.array([direction[1], direction[0], 0])
        east_vector = np.array([1, 0, 0])
        east_vector = coordinate_transformation(x_axis, east_vector)

        radiationProperties['solarLoadCoeffs']['startDay'] = startday
        radiationProperties['solarLoadCoeffs']['startTime'] = starttime
        radiationProperties['solarLoadCoeffs']['localStandardMeridian'] = localStandardMeridian
        radiationProperties['solarLoadCoeffs']['latitude'] = coordinates[0]
        radiationProperties['solarLoadCoeffs']['longitude'] = coordinates[1]
        if not np.isnan(east_vector).any():
            radiationProperties['solarLoadCoeffs']['gridEast'] = Vector(east_vector[0], east_vector[1], east_vector[2])
        radiationProperties.writeFile()

    def reconstruct(self):
        """Reconstruct the decomposed case. Executes OpenFOAM function reconstructPar in the case directory."""
        latesttimedirectory = os.path.join(self.name, self.getParallelTimes()[-1])

        if not os.path.exists(latesttimedirectory):
            os.system(os.path.join(self.name,"Reconstruct"))
            self._move_logs()
        else:
            print('Case is already reconstructed')

    def cpucores(self):
        """Return the number of used cpu cores, i.e. number of subdomains"""
        decomposeParDict = ParsedParameterFile(os.path.join(
                self.systemDir(), "decomposeParDict")
                )
        return int(decomposeParDict['numberOfSubdomains'])

    def change_number_cpucores(self, number):
        """Change the number of CPU cores that should be used for the simulation. 
        Can only be used before decomposing"""

        if number == self.cpucores():
            print("Number of CPU cores already set to {}. Doing nothing".format(number))
        elif not self.processorDirs():
            print("Number of CPU cores set to {}".format(number))

            decomposeParDict_system = ParsedParameterFile(os.path.join(
                self.systemDir(), "decomposeParDict")
                )
            decomposeParDict_airInside = ParsedParameterFile(os.path.join(
                self.systemDir(), "airInside", "decomposeParDict")
                )
            decomposeParDict_battery_template = ParsedParameterFile(
                os.path.join(self.systemDir(), "battery_template", "decomposeParDict")
                )

            list_decomposeParDicts = [
                decomposeParDict_system, 
                decomposeParDict_airInside, 
                decomposeParDict_battery_template
                ]

            for decomposeParDict in list_decomposeParDicts:
                decomposeParDict['numberOfSubdomains'] = number
                decomposeParDict.writeFile()
        else:
            raise Exception('Case already decomposed. Clean case before changing number of subdomains.')
        
    def postprocess(self):
        """
        Creates one postprocess file for every region out of function object postProcessing files.

        For every restart of solver OpenFOAM creates a new directory for postProcessing results. 
        This method creates single files for all timesteps and saves them in the transport directory. 
        """

        case_postProcessing = os.path.join(self.name, "postProcessing")
        targetpath_temperature = os.path.join(os.path.dirname(self.name), 'postProcessing', 'temperature')
        targetpath_wallHeatFlux =  os.path.join(os.path.dirname(self.name), 'postProcessing', 'wallHeatFlux')
        #Create new folders for postprocess results
        if not os.path.exists(targetpath_temperature):
            os.makedirs(targetpath_temperature)
        if not os.path.exists(targetpath_wallHeatFlux):
            os.makedirs(targetpath_wallHeatFlux)

        # Find all regions
        regions = self.regions()
        
        # Get all timesteps and delete last one, because for latestTime no postProcess folder exists
        times = self.getTimes()
        # If case is not reconstructed self.getTimes() only returns 0 directory, use parallel times instead
        if len(times) == 1:
            times = self.getParallelTimes()
        # Filter times so only times during transport are postprocessed
        times = [time for time in times if float(time) <= self.duration()]
        del times[-1]

        initial_temperature = ParsedParameterFile(
            os.path.join(self.name, '0', 'airInside', 'T')
            )['internalField'].val
    
        for i in range(len(regions)):
            # Add zero time head with initial temperatures
            df_head = {
                'time': 0,
                'average(T)': initial_temperature,
                'min(T)': initial_temperature,
                'max(T)': initial_temperature
            }
            df_temperature = pd.DataFrame(data = df_head, index = [0])
            df_wallHeatFlux = pd.DataFrame()

            for j in range(len(times)):
                # Create paths to files
                path_average = os.path.join(
                    case_postProcessing, regions[i], 'average_' + regions[i], times[j], 'volFieldValue.dat'
                    )
                path_min = os.path.join(
                    case_postProcessing, regions[i], 'min_' + regions[i], times[j], 'volFieldValue.dat'
                    )
                path_max = os.path.join(
                    case_postProcessing, regions[i], 'max_' + regions[i], times[j], 'volFieldValue.dat'
                    )
                path_wallHeatFlux = os.path.join(
                    case_postProcessing, 'airInside', 'wallHeatFlux', times[j], 'wallHeatFlux.dat'
                    )
                # Read as pandas dataframe
                average_temperature = pd.read_table(
                    path_average, sep="\s+", header=3, usecols = [0,1], names = ['time', 'average(T)']
                    )
                min_temperature = pd.read_table(
                    path_min, sep="\s+", header=3, usecols = [0,1], names = ['time', 'min(T)']
                    )
                max_temperature = pd.read_table(
                    path_max, sep="\s+", header=3, usecols = [0,1], names = ['time', 'max(T)']
                    )
                wallHeatFlux = pd.read_table(
                    path_wallHeatFlux, sep="\s+", header=1, usecols = [0,1,2,3,4], 
                    names = ['time', 'patch', 'min', 'max', 'integral']
                    )
                # Join temperatures to single file
                temperature = average_temperature.join(min_temperature['min(T)'])
                temperature = temperature.join(max_temperature['max(T)'])  
                # Select wallHeatFlux for the region
                if regions[i] == 'airInside':
                    wallHeatFlux = wallHeatFlux.loc[wallHeatFlux['patch'] == 'carrier']
                else:
                    wallHeatFlux = wallHeatFlux.loc[wallHeatFlux['patch'] == 'airInside_to_' + regions[i]]
                    # Heatflux in region is positive
                    wallHeatFlux.loc[:, ['min', 'max', 'integral']] = -1 * wallHeatFlux.loc[:, ['min', 'max', 'integral']]

                wallHeatFlux = wallHeatFlux.drop(columns = ['patch'])              

                df_temperature = pd.concat([df_temperature, temperature], ignore_index = True)
                df_wallHeatFlux = pd.concat([df_wallHeatFlux, wallHeatFlux], ignore_index = True)

            # Convert to Celsius
            df_temperature['average(T)'] = df_temperature['average(T)'] - 273.15
            df_temperature['min(T)'] = df_temperature['min(T)'] - 273.15
            df_temperature['max(T)'] = df_temperature['max(T)'] - 273.15

            filename_temperature = os.path.join(targetpath_temperature, regions[i] + '.csv')
            df_temperature.to_csv(filename_temperature, encoding='utf-8', index=False) 

            filename_wallHeatFlux = os.path.join(targetpath_wallHeatFlux, regions[i] + '.csv')
            df_wallHeatFlux.to_csv(filename_wallHeatFlux, encoding='utf-8', index=False) 

    def probe_freight(self, regionname):
        cargo_number, region_number = re.findall(r'\d+', regionname)

        # Read cargo if not existent
        if not hasattr(self, 'cargo'):
            json_filenames = [f for f in os.listdir(os.path.join(self.name, os.pardir)) if f.endswith('.json')]
            if len(json_filenames) != 1:
                raise ValueError('Should be only one json file in the transport directory')
            json_path = os.path.join(self.name, os.pardir, json_filenames[0])
            with open(json_path) as json_file: 
                json_dict = json.load(json_file, cls=TransportDecoder)
            self.cargo = [cargoDecoder(item) for item in json_dict['cargo']]

        battery_region = self.cargo[int(cargo_number)].battery_regions[int(region_number)]

        self.clear_probes()

        for i in range(battery_region.freight.elements_positions.shape[0]):
            self.add_probe(battery_region.freight.elements_positions[i, :])
        
        self.probe(regionname)
        self.clear_probes()
        
    def add_probe(self, location):
        """Add location of a new probe to probes file"""
        
        probefunction = os.path.join(self.systemDir(), 'probes')
        
        # Read the file into a list of lines
        with open(probefunction, 'r') as f:
            probefunction_lines = f.readlines()

        # Transform probe location in conform string
        probe = '(' + ' '.join(str(coordinate) for coordinate in location) + ')\n'

        # Add to right line
        probes = (probefunction_lines[-3].rstrip() + probe)
        probefunction_lines[-3] = probes

        # Write back to file
        with open(probefunction, 'w') as f:
            f.writelines(probefunction_lines)

    def clear_probes(self):
        """Clear all probe locations"""

        probefunction = os.path.join(self.systemDir(), 'probes')
        
        # Read the file into a list of lines
        with open(probefunction, 'r') as f:
            probefunction_lines = f.readlines()

        # Remove probes
        probefunction_lines[-3] = '\n'

        # Write back to file
        with open(probefunction, 'w') as f:
            f.writelines(probefunction_lines)

    def probe(self, region, location = None, time = None, clear = False):
        """
        Execute OpenFOAM postProcess function for probing a location for T value.
        Region of probe must be specified. 
        """
        if clear:
            self.clear_probes()

        if location != None: 
            self.add_probe(location)

        probespath = os.path.join(self.name, 'postProcessing', 'probes', region)

        if time == None:
            times = self.getParallelTimes()
            time = str(times[0]) + ':' + str(times[-1])
            probespath = os.path.join(probespath, '0', 'T')
        else:
            time = str(time)
            probespath = os.path.join(probespath, time, 'T')

        # Execute postProcess in reconstructed case, if processor folders are empty
        if os.path.basename(self.latestDir())== self.getParallelTimes()[-1]:
            command = 'postProcess -case {0} -time {1} -func probes -region {2} > {3}/log.probes'
            os.system(command.format(self.name, time, region, self.name))
        # Execute in decomposed case else
        elif len(self.getTimes()) < len(self.getParallelTimes()):
            number_processors = len(self.processorDirs())
            command = 'mpirun -np {0} postProcess -parallel -case {1} -time {2} -func probes -region {3} > {4}/log.probes'
            os.system(command.format(number_processors, self.name, time, region, self.name))
        else:
            raise OSError('Can not execute OpenFOAM postProcess utility. Check case for time directories')
        
        self._probes_to_csv(probespath, region)
        self._move_logs()

    def _probes_to_csv(self, probespath, region):

        targetdirectory = os.path.join(os.path.dirname(self.name), 'postProcessing', 'probes')
        #Create new folder for probes results
        if not os.path.exists(targetdirectory):
            os.makedirs(targetdirectory)

        probes = pd.read_table(probespath, sep="\s+",  header = None, comment = '#')

        # Rename column names, so naming fits probe number
        probes.columns = probes.columns.values - 1
        probes.rename(columns = {-1:'time'}, inplace = True) 

        # Convert Klevin to Celsius
        for columns in probes.columns.values[1:]:
            probes[columns] -= 273.15

        csvpath = os.path.join(targetdirectory, region + '.csv')
        # csvpath = os.path.dirname(probespath)
        # csvpath = os.path.join(csvpath, 'probes.csv')

        # Delete old file
        if os.path.exists(csvpath):
            os.remove(csvpath)

        # Write comments with probe locations
        with open(csvpath, 'a') as csvfile:
            with open(probespath) as f:
                i = 0
                while i < len(probes.columns):
                    probe = f.readline()
                    csvfile.write(probe)
                    i += 1

            probes.to_csv(csvfile, encoding='utf-8', index=False)

    def create_function_objects(self, battery_name, controlDict):
        """Create function objects for battery region. Needed for post processing."""
        
        # Copy function objects from template
        controlDict['functions']['average_' + battery_name] = copy.deepcopy(controlDict['functions']['average_battery0_0'])
        controlDict['functions']['min_' + battery_name] = copy.deepcopy(controlDict['functions']['min_battery0_0'])
        controlDict['functions']['max_' + battery_name] = copy.deepcopy(controlDict['functions']['max_battery0_0'])
        controlDict['functions']['wallTemperature_' + battery_name] = copy.deepcopy(controlDict['functions']['wallTemperature_battery0_0'])

        # Change region entry
        controlDict['functions']['average_' + battery_name ]['region'] = battery_name
        controlDict['functions']['min_' + battery_name]['region'] = battery_name
        controlDict['functions']['max_' + battery_name]['region'] = battery_name
        controlDict['functions']['wallTemperature_' + battery_name]['region'] = battery_name
        controlDict['functions']['wallTemperature_' + battery_name]['name'] = battery_name + '_to_airInside'

    def _move_logs(self):
        """Move log. files into logs folder"""
        logfolder = os.path.join(self.name, 'logs')
        logfiles = glob.iglob(os.path.join(self.name, "log.*"))
        for logfile in logfiles:
            logname = os.path.basename(logfile)
            logdestination = os.path.join(logfolder, logname)
            shutil.move(logfile, logdestination)  

    def pack(self, logs = True):
        """Compress case with solution time directories for better file transfer"""

        pack_path = os.path.join(
            os.path.dirname(self.name),
            'compressedCase'
        )

        additional = self.getTimes()
        additional.append('postProcessing')
        additional.append('case.foam')

        if not logs:
            exclude = ['logs']
        else:
            exclude = []

        self.packCase(pack_path, additional = additional, exclude = exclude)

    def plot(self, probes = None, tikz = False, format_ext = '.jpg', dpi = 250, marker = None):
        """Create plots for the simulation results"""
        self.load_weatherdata()
        add_seconds(self.weatherdata)
        
        postprocessing_path = os.path.join(self.name, os.pardir, 'postProcessing')
        plots_path = os.path.join(self.name, os.pardir, 'plots')
        pp_probes_path = os.path.join(postprocessing_path, 'probes')

        if not os.path.exists(plots_path):
            os.makedirs(plots_path)

        if probes != None:
            plot_probes_path = os.path.join(plots_path, 'probes')
            if not os.path.exists(plot_probes_path):
                os.makedirs(plot_probes_path)
            for probe in probes:
                probefile = os.path.join(pp_probes_path, probe + '.csv')
                # Create probe data
                self.probe_freight(probe)
                # Plot data
                df_probe = pd.read_csv(probefile, sep=',', comment='#')
                [plt.plot(df_probe['time'] / 3600, df_probe[str(i)], marker = marker) for i in range(df_probe.shape[1] - 1)]
                # Annotate plot
                plt.xlabel('time in h')
                plt.ylabel('temperature in °C')
                plt.grid(linestyle='--', linewidth=2, axis='y')
                # Save plot
                plotpath = os.path.join(plot_probes_path, probe + format_ext)
                plt.savefig(plotpath, dpi = dpi)
                if tikz:
                    self._tikz_plot(plotpath)
                plt.clf()

        # Plot average temperature of the air inside the carrier and ambient temperature
        pp_airInside_path = os.path.join(postprocessing_path, 'temperature', 'airInside.csv')
        df_airInside = pd.read_csv(pp_airInside_path)
        legendlabels = []
        plt.plot(df_airInside['time'] / 3600, df_airInside['average(T)'], marker = marker)
        legendlabels.append('average air temperature')
        # Plot ambient temperature
        plt.plot(self.weatherdata['seconds'] / 3600, self.weatherdata['T'],  marker = marker)
        legendlabels.append('ambient temperature')

        plt.xlabel('time in h')
        plt.ylabel('temperature in °C')
        plt.grid(linestyle='--', linewidth=2, axis='y')
        plt.legend(legendlabels, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol = 2)

        plotpath = os.path.join(plots_path, 'plot' + format_ext)
        plt.savefig(plotpath, dpi = dpi, bbox_inches='tight')
        if tikz:
            self._tikz_plot(plotpath)
        plt.clf()

        # Plot average temperature of cargo
        legendlabels = []
        battery_files = glob.iglob(os.path.join(postprocessing_path, 'temperature', 'battery*'))

        fig_average = plt.figure(1)
        fig_max = plt.figure(2)
        fig_min = plt.figure(3)

        ax_average = fig_average.add_subplot(111)
        ax_max = fig_max.add_subplot(111)
        ax_min = fig_min.add_subplot(111)

        ax_handles = [ax_average, ax_max, ax_min]
        
        for battery_file in battery_files:
            df_battery = pd.read_csv(battery_file)
            print(df_battery['max(T)'])
            ax_average.plot(df_battery['time'] / 3600, df_battery['average(T)'], marker = marker)
            ax_max.plot(df_battery['time'] / 3600, df_battery['max(T)'], marker = marker)
            ax_min.plot(df_battery['time'] / 3600, df_battery['min(T)'], marker = marker)
            legendlabels.append(os.path.splitext(os.path.basename(battery_file))[0])

        for ax_handle in ax_handles:
            ax_handle.set_xlabel('time in h')
            ax_handle.set_ylabel('temperature in °C')
            ax_handle.grid(linestyle='--', linewidth=2, axis='y')    
            ax_handle.legend(legendlabels, loc='center left', bbox_to_anchor=(1, 0.5), ncol = ceil(len(legendlabels) / 16))

        plotpath_average = os.path.join(plots_path, 'batteries_average' + format_ext)
        fig_average.savefig(plotpath_average, dpi = dpi, bbox_inches='tight')
        plotpath_max = os.path.join(plots_path, 'batteries_max' + format_ext)
        fig_max.savefig(plotpath_max, dpi = dpi, bbox_inches='tight')
        plotpath_min = os.path.join(plots_path, 'batteries_min' + format_ext)
        fig_min.savefig(plotpath_min, dpi = dpi, bbox_inches='tight')

        if tikz:
            self._tikz_plot(plotpath_average)     
            self._tikz_plot(plotpath_max)     
            self._tikz_plot(plotpath_min)     
     
    def _tikz_plot(self, plotpath):
            filename = os.path.splitext(os.path.basename(plotpath))[0] + '.pgf'
            plotpath = os.path.join(os.path.dirname(plotpath), 'tikz', filename)
            if not os.path.exists(os.path.dirname(plotpath)):
                os.makedirs(os.path.dirname(plotpath))
            tikzplotlib.save(plotpath, externalize_tables = True)
   
    def _save_data(self, data, filename):
        postProcessing_path = os.path.join(os.path.dirname(self.name), 'postProcessing')
        filepath = os.path.join(postProcessing_path, filename)
        with open(filepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        
    def duration(self):
        """Return the duration of the transport in seconds"""
        self.load_weatherdata()
        duration = self.weatherdata['Date'].iloc[-1] - self.weatherdata['Date'].iloc[0]
        return duration.total_seconds() 

    def _setup_arrival(self, ambienttemperature):
        # Remove fluid regions from the case (namely airInside region)
        regionProperties = ParsedParameterFile(os.path.join(self.constantDir(),'regionProperties'))
        regionProperties['regions'][1].clear()
        regionProperties.writeFile()

        # Disable function objects for airInside region
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
        controlDict['functions']['wallHeatFlux']['enabled'] = 'no'
        controlDict['functions']['wallTemperature_airInside']['enabled'] = 'no'
        controlDict['functions']['average_airInside']['enabled'] = 'no'
        controlDict['functions']['min_airInside']['enabled'] = 'no'
        controlDict['functions']['max_airInside']['enabled'] = 'no'
        controlDict.writeFile()

        self._change_dictionary_solids(ambienttemperature)
        
    def _change_dictionary_solids(self, ambienttemperature):
        # Change the changeDictionaryDict for all battery regions
        regions = self.regions()
        regions.remove('airInside')
        for region in regions:
            changeDictionaryDict = ParsedParameterFile(
                os.path.join(os.path.join(self.systemDir(), region, 'changeDictionaryDict'))
            )

            openfoam.external_wall['Ta'] = ambienttemperature
            openfoam.external_wall['h'] =  self.heattransfer_coefficient(ambienttemperature, 0, region = region)

            changeDictionaryDict['T']['boundaryField'][region + '_to_airInside'] = openfoam.external_wall

            if 'internalField' in changeDictionaryDict['T']:
                del changeDictionaryDict['T']['internalField']

            changeDictionaryDict.writeFile()

        os.system(os.path.join(self.name,"ChangeDictionarySolid"))
        self._move_logs()
 
    def _get_max_delta(self, reftemperature):
        """Calculate the maximal temperature difference of all solid regions to a reference temperature"""
        latesttime = self.getParallelTimes()[-2]
        path_postprocessing = os.path.join(self.name, "postProcessing")

        regions = self.regions()
        regions.remove('airInside')

        min_temperature = np.zeros(len(regions))
        max_temperature = np.zeros(len(regions))
        
        i = 0
        for region in regions:
            path_min = os.path.join(
                path_postprocessing, region, 'min_' + region, latesttime, 'volFieldValue.dat'
                )
            path_max = os.path.join(
                path_postprocessing, region, 'max_' + region, latesttime, 'volFieldValue.dat'
                )

            df_min = pd.read_table(
                path_min, sep="\s+", header=3, usecols = [1], names = ['min(T)']
                )
            df_max = pd.read_table(
                    path_max, sep="\s+", header=3, usecols = [1], names = ['max(T)']
                    )
            
            min_temperature[i] = df_min['min(T)'].iloc[-1]
            max_temperature[i] = df_max['max(T)'].iloc[-1]

            i += 1

        temperature = np.absolute(
            np.concatenate((min_temperature, max_temperature)) - reftemperature
            )
        return np.amax(temperature)

    def simulate_arrival(self, ambienttemperature):

        transportduration = self.duration()

        if transportduration > float(self.getParallelTimes()[-1]):
            raise ValueError('Transport simulation did not finish yet. Complete the transport before simulating arrival.')

        self._setup_arrival(ambienttemperature)

        deltaT = self._get_max_delta(ambienttemperature)
        max_deltaT = 1

        plot = False
        
        print('Initial temperature difference to ambienttemperature: {}'.format(deltaT))
        
        while deltaT > max_deltaT:
            print(deltaT)
            latesttime = float(self.getParallelTimes()[-1])
            controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
            controlDict['endTime'] = latesttime + 21600
            controlDict['writeInterval'] = 21600
            controlDict.writeFile()

            self._change_dictionary_solids(ambienttemperature)

            os.system(os.path.join(self.name,"Run"))
            self._move_logs()

            plt.plot((latesttime - transportduration) / 3600, deltaT)
            plot = True

            deltaT = self._get_max_delta(ambienttemperature)

        print('Finished simulation of arrival. Final difference to ambient temperature: {}'.format(deltaT))

        if plot:
            plotpath = os.path.join(os.path.dirname(self.name), 'plots', 'arrival.jpg')
            plt.axhline(y=ambienttemperature - 273.15, xmin=0, xmax= (latesttime - transportduration) / 3600)
            plt.savefig(plotpath, dpi = 250, bbox_inches='tight')

def utcoffset(utc_datetime, lat, lon):
    """Get the offset to UTC time at a specified location"""
    # Surpressing error output, because tzwhere uses depreciated numpy function
    with open(os.devnull, "w") as devnull:
        sys.stderr = devnull
        # find timezone at location
        timezone_str = tzwhere.tzwhere().tzNameAt(lat, lon)
        sys.stderr = sys.__stderr__
        
    print('Current timezone: {}'.format(timezone_str))
    timezone = pytz.timezone(timezone_str)
    offset = timezone.utcoffset(utc_datetime).total_seconds()/3600 
    return offset

def coordinate_transformation(x_axis, cart_vector):
    """
    Transform a vector in cartesian coordinates into 
    the coordinate system of with x-axis x_axis
    """
    angle = angle_between(x_axis, cart_vector)

    transformation = np.array([
        [ np.cos(angle), np.sin(angle), 0],
        [-np.sin(angle), np.cos(angle), 0],
        [             0,             0, 1]
    ]) 

    return np.matmul(transformation, cart_vector)

def unit_vector(vector):
    """Returns the unit vector of the vector"""
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2':

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))