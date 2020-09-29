import copy
from datetime import datetime, timedelta
import glob
import os
import re
import shutil

import geopy.distance
import numpy as np
import pandas as pd
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector

import modules.convection as convection

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
        self.addToClone('logs')


    def change_initial_temperature(self, temperature):
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

    def load_cargo(self, cargo):
        """Loads the carrier with cargo. New regions for cargo 
        are added to snappyHexMeshDict and regionProperties"""
        # refinementLevel for cargo regions
        refinementSurfacesLevel = [3,3]

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
            snappyHexMeshDict['castellatedMeshControls']['refinementSurfaces'].__setitem__(cargo_name, {'level': refinementSurfacesLevel})

            # Iteration over all individual battery regions in the cargo
            for j in range(len(cargo[i].batteries)):
                battery = cargo[i].batteries[j]
                battery.name = "battery" + str(i) + '_' + str(j)

                snappyHexMeshDict['castellatedMeshControls']['locationsInMesh'].append(
                    [battery.position, battery.name]
                    )

                # Copy the battery template folders 
                shutil.copytree(os.path.join(self.systemDir(), "battery_template"), os.path.join(self.systemDir(), battery.name))
                shutil.copytree(os.path.join(self.constantDir(), "battery_template"), os.path.join(self.name, "constant", battery.name))
                shutil.copytree(os.path.join(self.name, "0.org", "battery_template"), os.path.join(self.name, "0.org", battery.name))

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
        self.move_logs()

        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))

        # Delete internalField values, so values for the last timestep are not overwritten 
        # when OpenFOAM function changeDict is executed
        del changeDictionaryDict['T']['internalField']
        del changeDictionaryDict['U']['internalField']
        del changeDictionaryDict['p_rgh']['internalField']
        del changeDictionaryDict['p']['internalField']

        changeDictionaryDict.writeFile()

    def heattransfer_coefficient(self, T_U, u):
        """Calculate heattransfer coefficient"""
        # Value for current time is saved in folder for last time
        times = self.getParallelTimes()

        # If times has only one entry, that means only 0 folder exists, 
        # thus average path temperature is initial temperature
        if len(times) == 1:
            airInside0T = ParsedParameterFile(os.path.join(self.name, '0', 'airInside', 'T'))
            T_W = re.findall(r"[-+]?\d*\.\d+|\d+", str(airInside0T['internalField']))
            T_W = float(T_W[0])
        # Else use average patch temperature
        else:
            time = times[-2]
            path_averageTemperature = os.path.join(
                self.name,'postProcessing','airInside','temperature_right', str(time),'surfaceFieldValue.dat'
                )    
            df_patch_temperature = pd.read_table(
                path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T']
                )

            # OpenFOAM sometimes changes naming of surfaceFieldValue file, make sure that dataframe reads the data
            if df_patch_temperature.empty:
                path_averageTemperature = os.path.join(
                    self.name,'postProcessing','airInside','temperature_right',
                    str(time),'surfaceFieldValue_' + str(time) + '.dat'
                )
                df_patch_temperature = pd.read_table(
                    path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T']
                    )
            T_W = df_patch_temperature['T'].iloc[-1]

        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))
        if u < 1:
            # Length for natural convection is z-axis value of geometry of carrier
            L = snappyHexMeshDict['geometry']['carrier']['max'][2]
            return convection.coeff_natural(L, T_W, T_U), T_W
        else:
            # Length for forced convection is x-axis value of geometry of carrier
            L = snappyHexMeshDict['geometry']['carrier']['max'][0]
            return convection.coeff_forced(L, u), T_W

    def run(self):
        
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

        if latesttime == 0:
            startdate = pd.to_datetime(self.weatherdata['Date'].values[0])
            starttime = startdate.time()
            starttime = starttime.hour + starttime.minute / 60 + starttime.second / 3600
            startday = startdate.timetuple().tm_yday
            radiationProperties['solarLoadCoeffs']['startDay'] = startday
            radiationProperties['solarLoadCoeffs']['startTime'] = starttime

        current_timestamp = self.weatherdata['Date'].iloc[0] + timedelta(seconds = latesttime)

        i = self.weatherdata['Date'].sub(current_timestamp).abs().idxmin()

        while latesttime < transport_duration:
            # Read temperature and transform from Celsius to Kelvin
            temperature = self.weatherdata['T'].values[i] + 273.15

            current_time = pd.to_datetime(self.weatherdata['Date'].values[i]) 
            string_current_time = current_time.strftime('%Y-%m-%d_%H:%M:%S')

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

            #Upadate positon
            radiationProperties['solarLoadCoeffs']['latitude'] = coordinates[0]
            radiationProperties['solarLoadCoeffs']['longitude'] = coordinates[1]
            radiationProperties.writeFile()

            # Print to console            
            print('Date: {}'.format(string_current_time))
            print('Latitude: {0} Longitude: {1}'.format(coordinates[0], coordinates[1]))
            print('Temperature: {}'.format(temperature))
            print('Travelspeed: {}'.format(travelspeed))

            # Update the heattransfer coefficient 
            heattransfer_coefficient, T_W = self.heattransfer_coefficient(temperature, travelspeed)
            print('Recalculating heattransfer coefficient:')
            print('Heattransfer coeffcient: {0} with average wall temperature: {1}'.format(heattransfer_coefficient, T_W))

            # Write changes to changeDictionaryDict
            changeDictionaryDict['T']['boundaryField']['carrier'] = {
                'h': heattransfer_coefficient,
                'Ta': temperature,
            }
            changeDictionaryDict.writeFile()
            
            # Execute solver
            self.move_logs()
            os.system(os.path.join(self.name,"ChangeDictionary"))
            os.system(os.path.join(self.name,"Run"))

            #File management of log files
            target = os.path.join(self.name,"log.chtMultiRegionFoam" + '_' + string_current_time)
            shutil.move(path_solver_logfile, target)

            latesttime = float(self.getParallelTimes()[-1])
            i = i + 1

        print('Last timestep finished')
        self.move_logs()

    def reconstruct(self):
        """Reconstruct the decomposed case. Executes OpenFOAM function reconstructPar in the case directory."""
        latesttimedirectory = os.path.join(self.name, self.getParallelTimes()[-1])

        if not os.path.exists(latesttimedirectory):
            os.system(os.path.join(self.name,"Reconstruct"))
            self.move_logs()
        else:
            print('Case is already reconstructed')

    def cpucores(self, number):
        """Change the number of CPU cores that should be used for the simulation. 
        Can only be used before decomposing"""

        if not self.processorDirs():
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
        """Creates on post_process file for every region out of function object postProcessing files"""
        path_postProcessing = os.path.join(self.name, "postProcessing")
        path_PyFoam = os.path.join(path_postProcessing, 'PyFoam')
        #Create new folder for post_process results
        if not os.path.exists(path_PyFoam):
            os.makedirs(path_PyFoam)

        # Find all regions by direcotries in postProcessing, PyFoam folder is no region
        regions = os.listdir(path_postProcessing)
        regions.remove('PyFoam')
        
        # Get all timesteps and delete last one, because for latestTime no postProcess folder exists
        times = self.getTimes()
        del times[-1]

        for i in range(len(regions)):
            df_temperature = None
            for j in range(len(times)):
                path_average = os.path.join(path_postProcessing, regions[i], 'average_' + regions[i], times[j], 'volFieldValue.dat')
                path_min = os.path.join(path_postProcessing, regions[i], 'min_' + regions[i], times[j], 'volFieldValue.dat')
                path_max = os.path.join(path_postProcessing, regions[i], 'max_' + regions[i], times[j], 'volFieldValue.dat')
                    
                average_temperature = pd.read_table(path_average, sep="\s+", header=3, usecols = [0,1], names = ['time', 'average(T)'])
                min_temperature = pd.read_table(path_min, sep="\s+", header=3, usecols = [0,1], names = ['time', 'min(T)'])
                max_temperature = pd.read_table(path_max, sep="\s+", header=3, usecols = [0,1], names = ['time', 'max(T)'])

                temperature = average_temperature.join(min_temperature['min(T)'])
                temperature = temperature.join(max_temperature['max(T)'])                

                df_temperature = pd.concat([df_temperature, temperature], ignore_index = True)

            file_name = os.path.join(path_PyFoam, regions[i] + '_temperature')
            df_temperature.to_csv(file_name, encoding='utf-8', index=False)  

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


    def probe(self, location, region, time = None, clear = False):
        """
        Execute OpenFOAM postProcess function for probing a location for T value.
        Region of probe must be specified. 
        """
        if clear:
            self.clear_probes()

        self.add_probe(location)

        probespath = os.path.join(self.name, 'postProcessing', 'probes', region)

        if time == None:
            times = self.getParallelTimes()
            time = str(times[0]) + ':' + str(times[-1])
            probespath = os.path.join(probespath, '0', 'T')
        else:
            time = str(time)
            probespath = os.path.join(probespath, time, 'T')
            
        command = 'postProcess -case {0} -time {1} -func probes -region {2} > {3}/log.probes'
        os.system(command.format(self.name, time, region, self.name))
        probes_to_csv(probespath)
        self.move_logs()

    def create_function_objects(self, battery_name, controlDict):
        """Create function objects for battery region. Needed for post processing."""
        
        # Copy function objects from template
        controlDict['functions']['average_' + battery_name] = copy.deepcopy(controlDict['functions']['average_battery0_0'])
        controlDict['functions']['min_' + battery_name] = copy.deepcopy(controlDict['functions']['min_battery0_0'])
        controlDict['functions']['max_' + battery_name] = copy.deepcopy(controlDict['functions']['max_battery0_0'])

        # Change region entry
        controlDict['functions']['average_' + battery_name ]['region'] = battery_name
        controlDict['functions']['min_' + battery_name]['region'] = battery_name
        controlDict['functions']['max_' + battery_name]['region'] = battery_name

    def move_logs(self):
        """Move log. files into logs folder"""
        logfolder = os.path.join(self.name, 'logs')
        logfiles = glob.iglob(os.path.join(self.name, "log.*"))
        for logfile in logfiles:
            logname = os.path.basename(logfile)
            logdestination = os.path.join(logfolder, logname)
            shutil.move(logfile, logdestination)  

def probes_to_csv(probespath):
    probes = pd.read_table(probespath, sep="\s+",  header = None, comment = '#')

    # Rename column names, so naming fits probe number
    probes.columns = probes.columns.values - 1
    probes.rename(columns = {-1:'time'}, inplace = True) 

    # Convert Klevin to Celsius
    for columns in probes.columns.values[1:]:
        probes[columns] -= 273.15

    csvpath = os.path.dirname(probespath)
    csvpath = os.path.join(csvpath, 'probes.csv')

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


def setup(transport, initial_temperature = None, cpucores = 8, force_clone = True):
    """
    Function to setup OpenFOAM case for the transport. 
    Clones templatecase into the transport directory, loads the carrier with carg and creates mesh.
    """
    if transport.type == 'container':
        templatecase = Case(os.path.join('cases', 'container', 'container_template'))
    elif transport.type == 'carrier':
        templatecase = Case(os.path.join('cases', 'carrier_template'))
    else:
        print('Transport type not available. Check input json file.')
        
    casepath = os.path.join('transports', transport.name, 'case')
    if force_clone:
        case = templatecase.cloneCase(casepath)
    try:
        case = Case(casepath)
    except:
        print("Case does not exist: Creating new one")
        case = templatecase.cloneCase(casepath)

    airInside_polyMesh = os.path.join(case.constantDir(),'airInside', 'polyMesh')

    if not os.path.exists(airInside_polyMesh):
        if initial_temperature != None:
            print('Setting initial temperature for air and cargo to {} Kelvin'.format(initial_temperature))
            case.change_initial_temperature(initial_temperature)

        case.cpucores(cpucores)
        case.load_cargo(transport.cargo)
        case.create_mesh()

    else:
        print('Mesh already exists')
    
    case.load_weatherdata()

    return case



        


