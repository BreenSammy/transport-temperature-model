from contextlib import redirect_stdout
import copy
import csv   
from datetime import datetime, timedelta
import glob
import json
from math import ceil, floor
import os
import pytz
import re
import shutil
import sys

import geopy.distance
import numpy as np
import pandas as pd
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector
from scipy.spatial.transform import Rotation
import tikzplotlib
import timezonefinder
from tzwhere import tzwhere

import ttm.convection as convection
from ttm.cargo import cargoDecoder
import ttm.openfoam as openfoam
from ttm.route import direction_crossover, add_seconds
from ttm.transport import TransportDecoder
from ttm.weather import onsea


# Specific parameter values for different types of transports
TRANSPORTTYPES = {
    'container': {        
        'length': 6.0585,
        'width': 2.4390, 
        'height': 2.3855,
        'kappaLayers': 44,
        'thicknessLayers': 0.005,
        'absorptivity': 0.65
    },
    'container40': {        
        'length': 12.19205,
        'width': 2.4390, 
        'height': 2.3855,
        'kappaLayers': 44,
        'thicknessLayers': 0.005,
        'absorptivity': 0.65
    },
    'carrier': {
        'length': 13.0005,
        'width': 2.4610, 
        'height': 2.5505,
        'kappaLayers': 0.5,
        'thicknessLayers': 0.01,
        'absorptivity': 0.1
    },
    'car': {
        'length': 5,
        'width': 3, 
        'height': 3,
        'kappaLayers': 1,
        'thicknessLayers': 1,
        'absorptivity': 0.3
    }
}
# Max speed for natural convection
SPEEDTHERSHOLD = 4

SOLARINTENSITY = {
    '1': 1230,
    '2': 1215,
    '3': 1186,
    '4': 1136,
    '5': 1104,
    '6': 1088,
    '7': 1085,
    '8': 1107,
    '9': 1151,
    '10': 1192,
    '11': 1221,
    '12': 1233
}

EXTINCTIONCOEFFICENT = {
    '1': 0.142,
    '2': 0.144,
    '3': 0.156,
    '4': 0.180,
    '5': 0.196,
    '6': 0.205,
    '7': 0.207,
    '8': 0.201,
    '9': 0.177,
    '10': 0.160,
    '11': 0.149,
    '12': 0.142
}

class Case(SolutionDirectory):
    def __init__(self, name, archive = None, paraviewLink = True):
        SolutionDirectory.__init__(self, name, archive = None, paraviewLink = True)
        
        if not os.path.exists(os.path.join(self.name,'logs')):
            os.makedirs(os.path.join(self.name,'logs'))

        self.purge_write_switch = False

        #Add scripts and log folder to control simulation to cloneCase
        self.addToClone('Allrun.pre')
        self.addToClone('Run')
        self.addToClone('Reconstruct')
        self.addToClone('PostProcess')
        self.addToClone('ChangeDictionary')
        self.addToClone('ChangeDictionarySolid')
        self.addToClone('logs')

    def get_times(self):
        """Get all times with timedirectories, parallel or not"""
        # Get reconstructed times
        times = self.getTimes()
        # Use parallel times if latest parallel time is later than latest reconstructed time
        if times[-1] < self.getParallelTimes()[-1]:
            times = self.getParallelTimes()
        return times

    def latesttime(self):
        return float(self.get_times()[-1])

    def regions_in_latesttime(self):
        regions_in_latesttime = os.listdir(
            os.path.join(self.name, 'processor0', str(int(self.latesttime())))
            )
        if 'uniform' in regions_in_latesttime:
            regions_in_latesttime.remove('uniform')
        return regions_in_latesttime

    def duration(self):
        """Return the duration of the transport in seconds"""
        self.load_weatherdata()
        duration = self.weatherdata['Date'].iloc[-1] - self.weatherdata['Date'].iloc[0]
        return duration.total_seconds() 

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

    def initial_temperature(self):
        initial_temperature = ParsedParameterFile(
            os.path.join(self.name, '0', 'airInside', 'T')
            )['internalField'].val
        return initial_temperature

    def set_purge_write(self):
        """Set purge_write to true"""
        self.purge_write_switch = True

    def purge_write(self):
        """Delete the penultimate timestep so only two time directories are saved at any time"""
        times = self.get_times()
        # print(type(times[0]))
        if len(times) >= 2:
            processor_directories = glob.glob(os.path.join(self.name, 'processor*') + '/' + times[0])
            for directory in processor_directories:
                shutil.rmtree(directory)

    def change_transporttype(self, transporttype):
        """Change transport specific parameters"""

        if transporttype not in TRANSPORTTYPES:
            raise ValueError("Case.change_dimensions(): transporttype must be one of %r." % TRANSPORTTYPES)

        transport = TRANSPORTTYPES[transporttype]
        
        blockMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "blockMeshDict"))
        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))
        changeDictionaryDict = ParsedParameterFile(
            os.path.join(self.systemDir(), "airInside", "changeDictionaryDict")
            )
        boundaryRadiationProperties = ParsedParameterFile(
            os.path.join(self.constantDir(), "airInside", "boundaryRadiationProperties")
            )

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

        boundaryRadiationProperties['carrier'][
            'wallAbsorptionEmissionModel']['absorptivity'] = '( {0} {0} )'.format(transport['absorptivity'])
        boundaryRadiationProperties['carrier'][
            'wallAbsorptionEmissionModel']['emissivity'] = '( {0} {0} )'.format(transport['absorptivity'])

        blockMeshDict.writeFile()
        changeDictionaryDict.writeFile()
        snappyHexMeshDict.writeFile()
        boundaryRadiationProperties.writeFile()

    def switch_to_car(self):
        # Chech if case is valid
        if len(self.cargo_regions()) > 1:
            raise ValueError(
        'Simulation of car transport only works with one region. Please remove all but one cargo instances from transport.json'
        )
        self.remove_airInside()
        # Change the boundary condition of the battery region to a external wall
        changeDictionaryDict =  ParsedParameterFile(os.path.join(self.systemDir(), "battery0_0", "changeDictionaryDict"))
        # Apply a thermal resistance representing carbody
        openfoam.external_wall['kappaLayers'] = '( {} )'.format(TRANSPORTTYPES['car']['kappaLayers'])
        openfoam.external_wall['thicknessLayers'] = '( {} )'.format(TRANSPORTTYPES['car']['thicknessLayers'])
        changeDictionaryDict['T']['boundaryField']['battery0_0_to_airInside'] = openfoam.external_wall
        if 'internalField' in changeDictionaryDict['T']:
            del changeDictionaryDict['T']['internalField']
        changeDictionaryDict.writeFile()

        os.system(os.path.join(self.name,"ChangeDictionary") + ' battery0_0')

        self.load_weatherdata()
        if 'onsea' not in self.weatherdata.columns:
            print('Checking if waypoints are on sea or not')
            lats = self.weatherdata['Lat'].values
            lons = self.weatherdata['Lon'].values 
            self.weatherdata['onsea'] = [onsea(lats[i], lons[i]) for i in range(len(lats))] 
            self.weatherdata.to_csv(
                os.path.join(os.path.dirname(self.name), 'weatherdata.csv'), encoding='utf-8', index=False
                )
            
        self._move_logs()
    
    def load_cargo(self, cargo):
        """Loads the carrier with cargo. New regions for cargo 
        are added to snappyHexMeshDict and regionProperties"""
        # refinementLevel for cargo regions
        REFINEMENTSURFACELEVEL = [3,3]

        self.cargo = cargo
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
                if not os.path.exists(os.path.join(self.systemDir(), battery.name)):
                    shutil.copytree(os.path.join(self.systemDir(), "battery_template"), os.path.join(self.systemDir(), battery.name))
                if not os.path.exists( os.path.join(self.name, "constant", battery.name)):
                    shutil.copytree(os.path.join(self.constantDir(), "battery_template"), os.path.join(self.name, "constant", battery.name))
                if not os.path.exists( os.path.join(self.name, "0.org", battery.name)):
                    shutil.copytree(os.path.join(self.name, "0.org", "battery_template"), os.path.join(self.name, "0.org", battery.name))
                # Write thermophysical properties to the region
                thermophysicalProperties = ParsedParameterFile(os.path.join(self.constantDir(), battery.name, 'thermophysicalProperties'))
                thermophysicalProperties['mixture']['thermodynamics']['Cp'] = battery.thermal_capacity()
                thermophysicalProperties['mixture']['equationOfState']['rho'] = battery.density()
                thermophysicalProperties['mixture']['equationOfState']['rho'] = battery.density()
                thermalconductivity = battery.thermal_conductivity()
                thermophysicalProperties['mixture']['transport']['kappa'] = Vector(
                    thermalconductivity[0],
                    thermalconductivity[1],
                    thermalconductivity[2]
                    )
                thermophysicalProperties.writeFile()

                # Write boundary conditions for battery region and airInside region
                temperaturefile = ParsedParameterFile(os.path.join(self.name, "0.org", battery.name, 'T'))
                THICKNESS_CARTON = 0.01
                KAPPA_CARTON = 0.05 
                openfoam.region_coupling_solid_anisotrop['thicknessLayers'] = '( {} )'.format(THICKNESS_CARTON)
                openfoam.region_coupling_solid_anisotrop['kappaLayers'] = '( {} )'.format(KAPPA_CARTON)
                # changeDictionaryDict['T']['boundaryField'][battery.name + '_to_.*'] = openfoam.region_coupling_solid_anisotrop
                temperaturefile['boundaryField']['".*"'] = openfoam.region_coupling_solid_anisotrop
                temperaturefile.writeFile()

                changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), 'airInside', 'changeDictionaryDict'))
                openfoam.region_coupling_fluid['thicknessLayers'] = '( {} )'.format(THICKNESS_CARTON)
                # openfoam.region_coupling_fluid['thicknessLayers'] = '( {} )'.format(battery.packaging_thickness())
                openfoam.region_coupling_fluid['kappaLayers'] = '( {} )'.format(KAPPA_CARTON)
                # openfoam.region_coupling_fluid['kappaLayers'] = '( {} )'.format(battery.thermalconductivity_packaging)
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

    def _get_dominant_length(self, region, speed):
        """Get the dominant length for calculation of convection"""
        # Use dimesnions of carrier for airInside
        if region == 'airInside':
            snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))
            dimensions = snappyHexMeshDict['geometry']['carrier']['max']
        # And dimensions of cargo for cargo regions
        else:
            self.read_cargo()
            cargo_number, _ = re.findall(r'\d+', region)
            dimensions = self.cargo[int(cargo_number)].dimensions
        
        # Return z-axis value for natural convection
        if speed < SPEEDTHERSHOLD:
            return dimensions[2]
        # And x-axis value for forced convection
        else:
            return dimensions[0]

    def heattransfer_coefficient(self, T_U, u, region = 'airInside'):
        """Calculate heattransfer coefficient"""
        L = self._get_dominant_length(region, u)
        # Value for current time is saved in folder for last time
        times = self.getParallelTimes()

        # If times has only one entry, that means only 0 folder exists, 
        # thus average path temperature is initial temperature
        if times[-1] == '0':
            T_W = ParsedParameterFile(
                os.path.join(self.name, '0', 'airInside', 'T')
                )['internalField'].val
        # Else use average patch temperature
        else:
            wallTemperature_path = os.path.join(
                self.name,'postProcessing',region,'wallTemperature_' + region
                )
            timedirectories = sorted(os.listdir(wallTemperature_path), key = float)
            time = timedirectories[-1]

            path_averageTemperature = os.path.join(
                wallTemperature_path, str(time),'surfaceFieldValue.dat'
                )    
            # # OpenFOAM sometimes changes naming of surfaceFieldValue file, make sure that dataframe reads the data
            # if df_patch_temperature.empty:
            #     path_averageTemperature = os.path.join(
            #         self.name,'postProcessing',region,'wallTemperature_' + region,
            #         str(time),'surfaceFieldValue_' + str(time) + '.dat'
            #     )
            try: 
                df_patch_temperature = pd.read_table(
                    path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T']
                    )
            except FileNotFoundError:
                print(
                    """Last value for temperature of cargo carrier was not saved. 
                    Rerun or copy file from penultimate timestep to continue."""
                    )
            T_W = df_patch_temperature['T'].iloc[-1]

        if u < SPEEDTHERSHOLD:
            heattransfercoefficient = convection.coeff_natural(L, T_W, T_U)      
        else:
            heattransfercoefficient = convection.coeff_forced(L, u)

        # When heattranfercoefficient is too low, simulation gets unphysical (e.g. temperatures over 100 °C)
        if heattransfercoefficient < 0.2:
            heattransfercoefficient_path = os.path.join(
                os.path.dirname(self.name), 'postProcessing', 'heattransfercoefficient.csv'
                )
            df = pd.read_csv(heattransfercoefficient_path, names = ['time', 'heattransfercoefficient'])
            heattransfercoefficient = df.iloc[-1]['heattransfercoefficient']

        return heattransfercoefficient, T_W

    def run(self, borderregion = 'airInside'):
        """Execute the simulation"""
        if borderregion not in ['airInside', 'battery0_0']:
            raise ValueError('Only support for borderregions airInside for carrier transport or battery0_0 for car transport')

        self.load_weatherdata()
        
        path_solver_logfile = os.path.join(self.name,"log.chtMultiRegionFoam")

        # When solver restarts from other time than 0, remove solver logfile
        if os.path.exists(path_solver_logfile):
            os.remove(path_solver_logfile)

        # Open files that need to be modified
        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), borderregion, "changeDictionaryDict"))
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
        radiationProperties =  ParsedParameterFile(os.path.join(self.constantDir(), borderregion, "radiationProperties"))

        latesttime = self.latesttime()

        # Delete times that are not complete, needed if simulation stops before finished and is then restarted
        while sorted(self.regions_in_latesttime()) != sorted(self.regions()):
            processor_directories = glob.glob(os.path.join(self.name, 'processor*'))
            latesttime_processor_directories = [
                os.path.join(directory, str(int(latesttime))) for directory in processor_directories
                ]
            for directory in latesttime_processor_directories:
                shutil.rmtree(directory)
            latesttime = self.latesttime()

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
            writeinterval = np.floor(endTime_delta)
            controlDict['writeInterval'] = writeinterval
            controlDict['endTime'] = latesttime + endTime_delta
            # Limit timesteps to fixed value for small writeintervals, or timesteps can be bigger than writeInterval
            if writeinterval < 1000:
                controlDict['adjustTimeStep'] = 'no'
            else:
                controlDict['adjustTimeStep'] = 'yes'
            controlDict.writeFile()

            # Calculate travelspeed between waypoints
            coordinates = self.weatherdata[['Lat', 'Lon']].values[i]
            coordinates_next = self.weatherdata[['Lat', 'Lon']].values[i+1]
            distance = geopy.distance.distance(coordinates, coordinates_next).m
            travelspeed = distance / endTime_delta
            # Set travelspeed to 0 for cartransports on sea, because car is inside ship
            if borderregion == 'battery0_0':
                if self.weatherdata['onsea'].values[i] == True:
                    travelspeed = 0

            # #Upadate positon
            self._update_radiationProperties(
                radiationProperties, current_timestamp, coordinates, coordinates_next
                )

            heattransfer_coefficient, T_W = self.heattransfer_coefficient(temperature, travelspeed, region = borderregion)
            # Write changes to changeDictionaryDict
            if borderregion == 'airInside':
                changeDictionaryDict['T']['boundaryField'] = {}
                changeDictionaryDict['T']['boundaryField']['carrier'] = {
                    'h': heattransfer_coefficient,
                    'Ta': temperature,
                }
                changeDictionaryDict['T']['boundaryField']['bottom'] = {
                    'Ta': temperature
                }
            elif borderregion == 'battery0_0':
                changeDictionaryDict['T']['boundaryField'] = {}
                changeDictionaryDict['T']['boundaryField']['battery0_0_to_airInside'] = {
                    'h': heattransfer_coefficient,
                    'Ta': temperature,
                }
            changeDictionaryDict.writeFile()
            
            # Print to console            
            print('Timestamp: {} (UTC)'.format(string_current_timestamp))
            print('Latitude: {0} Longitude: {1}'.format(round(coordinates[0], 3), round(coordinates[1], 3)))
            print('Temperature: {}'.format(round(temperature, 1)))
            print('Travelspeed: {}'.format(round(travelspeed, 2)))
            print('Heattransfer coeffcient: {0} with average wall temperature: {1}'.format(round(heattransfer_coefficient, 2), round(T_W, 1)))

            #Write travelspeed and heattransfercoeffiecient to file
            self._save_data([latesttime, travelspeed], 'speed.csv')
            self._save_data([latesttime, heattransfer_coefficient], 'heattransfercoefficient.csv')

            # Execute solver
            self._move_logs()
            os.system(os.path.join(self.name,"ChangeDictionary") + ' ' + borderregion)
            os.system(os.path.join(self.name,"Run"))

            # Purge write
            if self.purge_write_switch == True:
                self.purge_write() 

            #File management of log files
            target = os.path.join(self.name,"log.chtMultiRegionFoam" + '_' + string_current_timestamp)
            shutil.move(path_solver_logfile, target)

            latesttime = float(self.getParallelTimes()[-1])
            i = i + 1

        print('Last timestep finished')
        self._move_logs()

    def _update_radiationProperties(
        self, radiationProperties, timestamp, coordinates, coordinates_next
        ):
        startdate = self.weatherdata['Date'].iloc[0]
        # Get offset to UTC time
        localStandardMeridian = utcoffset(
            timestamp, coordinates[0], coordinates[1]
            )
        if localStandardMeridian != None:
            # Transform UTC time to local time
            startdate += timedelta(hours = localStandardMeridian)
            # Get time in decimal format
            starttime = startdate.time()
            starttime = starttime.hour + starttime.minute / 60 + starttime.second / 3600
            # Get startday as the number of the day in given year
            startday = startdate.timetuple().tm_yday
       
            radiationProperties['solarLoadCoeffs']['startDay'] = startday
            radiationProperties['solarLoadCoeffs']['startTime'] = starttime
            radiationProperties['solarLoadCoeffs']['localStandardMeridian'] = localStandardMeridian

        radiationProperties['radiation'] = 'on'
        radiationProperties['solarLoadCoeffs']['latitude'] = coordinates[0]
        radiationProperties['solarLoadCoeffs']['longitude'] = coordinates[1]
        radiationProperties['solarLoadCoeffs']['A'] = SOLARINTENSITY[str(timestamp.month)]
        radiationProperties['solarLoadCoeffs']['B'] = EXTINCTIONCOEFFICENT[str(timestamp.month)]
        # Calculate vector for east in grid coordinates
        direction = direction_crossover(coordinates, coordinates_next)
        # latitude matches y, longitude matches x
        x_axis = np.array([direction[1], direction[0], 0])
        east_vector = np.array([1, 1, 0])
        east_vector = east_vector / np.linalg.norm(east_vector)
        east_vector = coordinate_transformation(x_axis, east_vector)
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

    def postprocess(self, arrival = False):
        case_postProcessing = os.path.join(self.name, "postProcessing")
        targetpath_wallHeatFlux =  os.path.join(os.path.dirname(self.name), 'postProcessing', 'wallHeatFlux')

        # Find all regions
        regions = os.listdir(case_postProcessing)

        if 'probes' in regions:
            regions.remove('probes')
        
        times = self.get_times()
        # Filter times for either before or after arrival
        if arrival:
            lasttransporttime = times[times.index(str(int(self.duration()))) - 1]
            times = [time for time in times if float(time) >= self.duration()]
            regions.remove('airInside')
            targetpath = os.path.join(os.path.dirname(self.name), 'postProcessing', 'arrival')
        else:
            times = [time for time in times if float(time) <= self.duration()]
            targetpath = os.path.join(os.path.dirname(self.name), 'postProcessing', 'temperature')
        # If times is empty stop
        if not times:
            raise ValueError('No times to postprocess')

        # Header length for different types of postprocessing resultes from OpenFOAM
        header = {
            'volFieldValue.dat': 3,
            'surfaceFieldValue.dat': 4,
            'wallHeatFlux.dat': 1
        }
        
        # Iterate over regions
        for region in regions:
            region_path = os.path.join(case_postProcessing, region)
            postprocess_function_paths = [os.path.join(region_path, x) for x in os.listdir(region_path)]
            result = pd.DataFrame()
            # result = pd.DataFrame(data = {'time': times})
            # if region = 
            # Iterate over results from different postprocess functions 
            for path in postprocess_function_paths:
                # Get paths to all postprocessing files
                all_timedirectories = os.listdir(path)
                if not self.purge_write_switch or arrival:
                    # Select only timedirectories until penultimate, because postprocessing results for current time are saved in lasttime
                    all_selectedtimedirectories = sorted(
                        set(times[0:-1]).intersection(all_timedirectories), key = float
                        )
                else:
                    all_selectedtimedirectories = sorted(set(all_timedirectories[0:-1]), key = float)

                all_paths = [os.path.join(path, x) for x in all_selectedtimedirectories]
                filename = os.listdir(all_paths[0])[0]
                all_paths = [os.path.join(x, filename) for x in all_paths]
                if all_paths == []:
                    raise ValueError('No results to postprocess available')
                # Define column name for dataframe
                colname = os.path.basename(path).split('_')[0] + '(T)'
                
                # Handle wallHeatFLux files different
                if os.path.basename(path) == 'wallHeatFlux':
                    column_names = ['time', 'patch', 'min', 'max', 'integral']
                    wallHeatFlux_list = (
                        [pd.read_csv(
                            f, 
                            sep="\s+", 
                            header=header[filename], 
                            usecols = range(len(column_names)), 
                            names = column_names
                            ) for f in all_paths]
                        )
                    wallHeatFlux = pd.concat(wallHeatFlux_list)
                    wallHeatFlux.index = range(len(wallHeatFlux))
                    patches = wallHeatFlux.patch.unique()
                    # Sort by patches 
                    for patch in patches:
                        df_patch = wallHeatFlux.loc[wallHeatFlux['patch'] == patch]
                        df_patch = df_patch.drop(columns = ['patch'])
                        # Correct sign of heatflux, positive for flux into domain
                        if patch != 'carrier':
                            df_patch.loc[:, ['min', 'max', 'integral']] = -1 * df_patch.loc[:, ['min', 'max', 'integral']]
                        filename_wallHeatFlux = os.path.join(targetpath_wallHeatFlux, patch + '.csv')
                        df_patch.to_csv(filename_wallHeatFlux, encoding='utf-8', index=False) 
                    
                else:
                    # Get the first temperature at arrival, hence the last of the transport
                    if arrival:
                        lasttransportpath = os.path.join(path, lasttransporttime, filename)
                        df_lasttransport = pd.read_csv(
                            lasttransportpath, sep="\s+", header=header[filename],
                            usecols = [0,1], names = ['time', colname], 
                            dtype={'time': str, 'colname': float}
                            )
                        initial_temperature = df_lasttransport[colname].iloc[0]
                        dict_head = {
                            'time': times[0],
                            colname: initial_temperature,
                            }
                    else:
                        initial_temperature = self.initial_temperature()
                        dict_head = {
                            'time': '0',
                            colname: initial_temperature,
                            }

                    # Read data from files and save in one dataframe
                    df_list = [pd.DataFrame( data = dict_head, index=[0])]
                    df_list.extend(
                        [pd.read_csv(
                            f, sep="\s+", header=header[filename], 
                            usecols = [0,1], names = ['time', colname], 
                            dtype={'time': str, 'colname': float}
                            ) for f in all_paths]
                        )
                    df = pd.concat(df_list)
                    # Join the dataframes together into one
                    df.index = range(len(df))
                    # Convert to Celsius
                    df[colname] = df[colname] - 273.15
                    if result.empty:
                        result['time'] = df['time']
                    # Join with other postprocessing results
                    result = pd.merge(result, df, how='outer')

            # Save as csv
            result.to_csv(os.path.join(targetpath, region + '.csv'), index=False, encoding='utf-8')
        
        # Calculate average data for all cargo regions
        transport_postProcessing = os.path.join(os.path.dirname(self.name), 'postProcessing')
        cargodata_path = os.path.join(transport_postProcessing, 'temperature', 'cargo.csv')
        paths = glob.glob(transport_postProcessing + '/temperature/battery*.csv')
        n = 0
        df_list_average = []
        df_list_min = []
        df_list_max = []
        time = pd.read_csv(paths[0], usecols=['time'])
        for path in paths:
            df_average = pd.read_csv(path, usecols=['average(T)'])
            df_average.columns = [str(n)]
            df_list_average.append(df_average)
            df_min = pd.read_csv(path, usecols=['min(T)'])
            df_min.columns = [str(n)]
            df_list_min.append(df_min)
            df_max = pd.read_csv(path, usecols=['max(T)'])
            df_max.columns = [str(n)]
            df_list_max.append(df_max)
            n += 1

        df_average = pd.concat(df_list_average, axis = 1, ignore_index = False, join = 'inner')
        df_average['average(T)'] = df_average.mean(axis=1)
        df_min = pd.concat(df_list_min, axis = 1, ignore_index = False, join = 'inner')
        df_min['min(T)'] = df_min.mean(axis=1)
        df_max = pd.concat(df_list_max, axis = 1, ignore_index = False, join = 'inner')
        df_max['max(T)'] = df_max.mean(axis=1)

        cargo_temperature = pd.concat(
            [time, df_average['average(T)'], df_min['min(T)'], df_max['max(T)']],
            axis = 1, ignore_index = False, join = 'inner'
        )
        cargo_temperature.to_csv(
            cargodata_path, 
            encoding='utf-8', 
            index=False
            )


    def read_cargo(self):
        # Read cargo if not existent
        if not hasattr(self, 'cargo'):
            json_filenames = [f for f in os.listdir(os.path.join(self.name, os.pardir)) if f.endswith('.json')]
            if len(json_filenames) != 1:
                raise ValueError('Should be only one json file in the transport directory')
            json_path = os.path.join(self.name, os.pardir, json_filenames[0])
            with open(json_path) as json_file: 
                json_dict = json.load(json_file, cls=TransportDecoder)
            self.cargo = [cargoDecoder(item) for item in json_dict['cargo']]

    def probe_freight(self, region):
        regions = self.cargo_regions()
        if region not in regions:
            raise ValueError('Region {} not exisent. Try one of {}'.format(region, regions))

        cargo_number, region_number = re.findall(r'\d+', region)

        self.read_cargo()

        battery_region = self.cargo[int(cargo_number)].battery_regions[int(region_number)]

        self.clear_probes()

        for i in range(battery_region.freight.elements_positions.shape[0]):
            self.add_probe(battery_region.freight.elements_positions[i, :])
        
        self.probe(region)
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

    def _execute_probe_postprocess(self, time, region):
        # Execute postProcess in reconstructed case, if processor folders are empty
        if os.path.basename(self.latestDir()) == self.getParallelTimes()[-1]:
            command = 'postProcess -case {0} -time {1} -func probes -region {2} > {3}/log.probes'
            os.system(command.format(self.name, time, region, self.name))
        # Execute in decomposed case else
        elif len(self.getTimes()) < len(self.getParallelTimes()):
            number_processors = len(self.processorDirs())
            command = 'mpirun -np {0} postProcess -parallel -case {1} -time {2} -func probes -region {3} > {4}/log.probes'
            os.system(command.format(number_processors, self.name, time, region, self.name))
        else:
            raise OSError('Can not execute OpenFOAM postProcess utility. Check case for time directories')

    def probe_from_file(self, filepath):
        """
        Use coordinates specified in a .csv file to probe case for T values

        Example file:
        region,x,y,z
        airInside,3,1,2
        battery0_0,3,2,2
        """
        print('Probeing case from file')
        probe_locations = pd.read_csv(filepath)
        grouped_probe_locations = probe_locations.groupby(probe_locations.region)
        times = self.get_times()
        time = str(times[0]) + ':' + str(times[-1])

        for groupkey in grouped_probe_locations.groups:
            region = groupkey
            probespath = os.path.join(self.name, 'postProcessing', 'probes', region, '0', 'T')
            df = grouped_probe_locations.get_group(groupkey) 
            locations = df.loc[:,['x','y','z']].values
            [self.add_probe(locations[i,:]) for i in range(locations.shape[0])]
            self._execute_probe_postprocess(time, region)
            self._probes_to_csv(probespath, region)
            self._move_logs()
            self.clear_probes()

    def probe(self, region, location = None, time = None, clear = False):
        """
        Execute OpenFOAM postProcess function for probing a location for T value.
        Region of probe must be specified. 
        """

        print('Probeing case')
        regions = self.regions()
        if region not in regions:
            raise ValueError('Region {} not exisent. Try one of {}'.format(region, regions))

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

        self._execute_probe_postprocess(time, region)
        
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
        print("Compressing case files")

        pack_path = os.path.join(
            os.path.dirname(self.name),
            'compressedCase'
        )

        additional = self.getTimes()
        # additional.append('postProcessing')
        # additional.append('case.foam')

        if not logs:
            exclude = ['logs']
        else:
            exclude = []

        # self.packCase(pack_path, additional = additional, exclude = exclude)
        self.packCase(pack_path, additional = additional)
        # self.packCase(pack_path)
   
    def _save_data(self, data, filename):
        postProcessing_path = os.path.join(os.path.dirname(self.name), 'postProcessing')
        filepath = os.path.join(postProcessing_path, filename)
        with open(filepath, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(data)
        
    def cargo_regions(self):
        """Return all cargo regions of the case"""
        regions = self.regions()
        regions.remove('airInside')
        return regions
    
    def remove_airInside(self):
        """Remove fluid regions from the case (namely airInside region)"""
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

    def _setup_arrival(self, ambienttemperature):
        self.remove_airInside()

        self._change_dictionary_solids(ambienttemperature)
        
    def _change_dictionary_solids(self, ambienttemperature):
        # Change the changeDictionaryDict for all battery regions
        regions = self.cargo_regions()
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
 
    def _get_max_delta(self, reftemperature, extrem = False):
        """Calculate the maximal temperature difference of all solid regions to a reference temperature"""
        # print(self.getParallelTimes())
        # Catch if case did no transport
        if self.getParallelTimes() == ['0']:
            return abs(self.initial_temperature() - reftemperature)

        # latesttime = self.getParallelTimes()[-2]
        path_postprocessing = os.path.join(self.name, "postProcessing")

        regions = self.regions()
        regions.remove('airInside')
        latesttime = sorted(
            set(os.listdir(os.path.join(path_postprocessing, 'battery0_0','max_battery0_0'))), 
            key = float
            )[-1]

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
        if extrem:
            # Determin which temperature is furthest from reftemperature
            maximum = np.amax(max_temperature)
            minimum = np.amax(min_temperature)
            if maximum < reftemperature:
                extremum = maximum
            else:
                extremum = minimum
            return np.amax(temperature), extremum
        else:
            return np.amax(temperature)

    def simulate_arrival(self, ambienttemperature):
        """Simulate heat exchange at arrival of cargo at destination"""
        
        print('Starting simulation of arrival')
        # Transform from Celsius to Kelvin
        ambienttemperature += 273.15
        
        transportduration = self.duration()

        if transportduration > float(self.getParallelTimes()[-1]):
            raise ValueError('Transport simulation did not finish yet. Complete the transport before simulating arrival.')

        deltaT = self._get_max_delta(ambienttemperature)
        
        max_deltaT = 1
        timestep = 14400
        df_list = []
        print('Initial temperature difference to ambient temperature: {}'.format(deltaT))
        
        if deltaT > max_deltaT:
            self._setup_arrival(ambienttemperature)
        
        while deltaT > max_deltaT:
            print('Temperature difference to ambient temperature: {}'.format(deltaT))
            latesttime = float(self.getParallelTimes()[-1])
            controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
            controlDict['endTime'] = latesttime + timestep
            controlDict['writeInterval'] = timestep
            controlDict.writeFile()

            self._change_dictionary_solids(ambienttemperature)

            os.system(os.path.join(self.name,"Run"))
            self._move_logs()
   
            deltaT, temperature_extrem = self._get_max_delta(ambienttemperature, extrem=True)

            df = pd.DataFrame(
                data = {
                    'time': latesttime,
                    'temperature': temperature_extrem - 273.15
                }, 
                index = [0]
                )

            df_list.append(df)

        print('Finished simulation of arrival. Final difference to ambient temperature: {}'.format(deltaT))
        if df_list != []:
            path = os.path.join(os.path.dirname(self.name), 'postProcessing', 'arrival', 'arrival.csv')
            df = pd.concat(df_list)
            # Normalize first time to 0
            df['time'] = df['time'] - df['time'].iloc[0]
            df.to_csv(path, encoding='utf-8', index=False)
            
def utcoffset(utc_datetime, lat, lon):
    """Get the offset to UTC time at a specified location"""
    # Get timezone name
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
    if timezone_str == None:
        print('Current timezone: No match for location. Probably on sea. Approximating timezone.')
        #rough approximation can be calculated: 1 hour difference corresponds to 15 degrees longitude (360 / 24).
        return floor(lon/15)

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