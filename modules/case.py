import copy
from datetime import datetime
import glob
import os
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
        
        print(self.name)

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

        changeDictionaryDict_airInside['T']['internalField'] = temperature
        changeDictionaryDict_battery['T']['internalField'] = temperature

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

    def heattransfer_coefficient(self, T_U, u):
        """Calculate heattransfer coefficient"""
        # Value for current time is saved in folder for last time
        times = self.getParallelTimes()
        time = times[-2]

        path_averageTemperature = os.path.join(
            self.name,'postProcessing','airInside','temperature_right', str(time),'surfaceFieldValue.dat'
            )    

        df_patch_temperature = pd.read_table(path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T'])

        # OpenFOAM sometimes changes naming of surfaceFieldValue file, make sure that dataframe reads the data
        if df_patch_temperature.empty:
            path_averageTemperature = os.path.join(
                self.name,'postProcessing','airInside','temperature_right', str(time),'surfaceFieldValue_' + str(time) + '.dat'
            )
            df_patch_temperature = pd.read_table(path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T'])

        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))
        T_W = df_patch_temperature['T'].iloc[-1]
        if u < 1:
            # Length for natural convection is z-axis value of geometry of carrier
            L = snappyHexMeshDict['geometry']['carrier']['max'][2]
            return convection.coeff_natural(L, T_W, T_U), T_W
        else:
            # Length for forced convection is x-axis value of geometry of carrier
            L = snappyHexMeshDict['geometry']['carrier']['max'][0]
            return convection.coeff_forced(L, u), T_W

    def run(self):

        # Open files that need to be modified
        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
        radiationProperties =  ParsedParameterFile(os.path.join(self.constantDir(), "airInside", "radiationProperties"))

        # Delete internalField values, so the last timestep does not get overwritten
        del changeDictionaryDict['T']['internalField']
        del changeDictionaryDict['U']['internalField']
        del changeDictionaryDict['p_rgh']['internalField']
        del changeDictionaryDict['p']['internalField']

        time = controlDict['endTime']

        if time == 0:
            startdate = pd.to_datetime(self.weatherdata['Date'].values[0])
            starttime = startdate.time()
            starttime = starttime.hour + starttime.minute / 60 + starttime.second / 3600
            startday = startdate.timetuple().tm_yday
            radiationProperties['solarLoadCoeffs']['startDay'] = startday
            radiationProperties['solarLoadCoeffs']['startTime'] = starttime

        for i in range(len(self.weatherdata.index)-1):
            # Read temperature and transform from Celsius to Kelvin
            temperature = self.weatherdata['T'].values[i] + 273.15
            time = controlDict['endTime']

            coordinates = self.weatherdata[['Lat', 'Lon']].values[i]
            coordinates_next = self.weatherdata[['Lat', 'Lon']].values[i+1]

            distance = geopy.distance.distance(coordinates, coordinates_next).m

            # Update endTime of the simulation
            endTime_delta = self.weatherdata['Date'].values[i+1] - self.weatherdata['Date'].values[i]
            endTime_delta = endTime_delta / np.timedelta64(1, 's')

            travelspeed = distance / endTime_delta

            print(travelspeed)

            controlDict['writeInterval'] = np.floor(endTime_delta)
            controlDict['endTime'] = controlDict['endTime'] + endTime_delta
            controlDict.writeFile()

            #Upadate positon
            radiationProperties['solarLoadCoeffs']['latitude'] = self.weatherdata['Lat'].values[i]
            radiationProperties['solarLoadCoeffs']['longitude'] = self.weatherdata['Lon'].values[i]
            radiationProperties.writeFile()

            # Update the heattransfer coefficient 
            if time != 0:
                heattransfer_coefficient, T_W = self.heattransfer_coefficient(temperature, travelspeed)
                print(
                    'Recalculating heattransfer coefficient: \n' +
                    'Heattransfer coeffcient: ' + str(heattransfer_coefficient) + ' with average wall temperature: ' + str(T_W)
                    )
                changeDictionaryDict['T']['boundaryField']['carrier']['h'] = heattransfer_coefficient

            # Update ambient temperature
            changeDictionaryDict['T']['boundaryField']['carrier']['Ta'] = temperature
            changeDictionaryDict.writeFile()
            
            # Execute solver
            os.system(os.path.join(self.name,"ChangeDictionary"))
            os.system(os.path.join(self.name,"Run"))

            #File management of log files
            timestep = pd.to_datetime(self.weatherdata['Date'].values[i]) 
            string_timestep = timestep.strftime('%Y-%m-%d_%H:%M:%S')
            original = os.path.join(self.name,"log.chtMultiRegionFoam")
            target = os.path.join(self.name,"log.chtMultiRegionFoam" + '_' + string_timestep)
            shutil.move(original, target)
        
        self.move_logs()

    def reconstruct(self):
        """Reconstruct the decomposed case. Executes OpenFOAM function reconstructPar in the case directory."""
        os.system(os.path.join(self.name,"Reconstruct"))

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
            shutil.move(logfile, logfolder)  


def setup(transport, force_clone = True):
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
        case.load_cargo(transport.cargo)
        case.create_mesh()
    
    case.load_weatherdata()

    return case



        


