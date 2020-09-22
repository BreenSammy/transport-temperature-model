import copy
import os
import shutil

import numpy as np
import pandas as pd
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector

import modules.convection as convection

class Case(SolutionDirectory):
    def __init__(self, name, archive=None, paraviewLink=False):
        SolutionDirectory.__init__(self, name, archive=None, paraviewLink=False)

        if not os.path.exists(os.path.join(self.name,'logs')):
            os.makedirs(os.path.join(self.name,'logs'))

        #Add scripts and log folder to control simulation to cloneCase
        self.addToClone('Allrun.pre')
        self.addToClone('Run')
        self.addToClone('Reconstruct')
        self.addToClone('PostProcess')
        self.addToClone('logs')

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
            cargo[i].move_STL(self, cargo[i].name + '.stl')

            # Adding current cargo to the snappyHexMeshDict
            snappyHexMeshDict['geometry'].__setitem__(cargo[i].name + '.stl', {'type': 'triSurfaceMesh', 'name': cargo[i].name})
            snappyHexMeshDict['castellatedMeshControls']['refinementSurfaces'].__setitem__(cargo[i].name, {'level': refinementSurfacesLevel})

            # Iteration over all individual battery regions in the cargo
            for j in range(len(cargo[i].batteries)):
                battery = cargo[i].batteries[j]
                battery.name = "battery" + str(i) + '_' + str(j)
                battery_system_path = os.path.join(self.systemDir(), battery.name)

                snappyHexMeshDict['castellatedMeshControls']['locationsInMesh'].append(
                    [battery.position, battery.name])

                # Copy the battery template folders 
                shutil.copytree(os.path.join(self.systemDir(), "battery_template"), battery_system_path)
                shutil.copytree(os.path.join(self.constantDir(), "battery_template"), os.path.join(self.name, "constant", battery.name))
                shutil.copytree(os.path.join(self.name, "0.org", "battery_template"), os.path.join(self.name, "0.org", battery.name))
                # os.system('cp -r ' + os.path.join(self.systemDir(), "battery_template") + " " + battery_system_path)
                # os.system('cp -r ' + os.path.join(self.constantDir(), "battery_template") + " " + os.path.join(self.name, "constant", battery.name))
                # os.system('cp -r ' + os.path.join(self.name, "0.org", "battery_template") + " " + os.path.join(self.name, "0.org", battery.name))

                #Names of the solid regions are in third entry of the list regions, adding batteries
                regionProperties['regions'][3].append(battery.name)

                self.create_function_objects(battery.name, controlDict)

        regionProperties.writeFile()
        snappyHexMeshDict.writeFile()
        controlDict.writeFile()

    # def remove_cargo(self):

    def create_mesh(self):
        os.system(os.path.join(self.name,"Allrun.pre"))

    def heattransfer_coefficient(self, time, L, T_U):
        # Value for current time is saved in folder for last time, thus minus 1h
        time = time - 3600
        path_averageTemperature = os.path.join(
            self.name,'postProcessing','airInside','temperature_right',str(time),'surfaceFieldValue.dat'
            )    
        df_patch_temperature = pd.read_table(path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T'])
        T_W = df_patch_temperature['T'].iloc[-1]
        return convection.coeff_natural(L, T_W, T_U)

    def run(self, ambientTemperature):

        # Open files that need to be modified
        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
        
        for i in range(len(ambientTemperature)):
            time = controlDict['endTime']
            # Update the heattransfer coefficient 
            if time != 0:
                print(self.heattransfer_coefficient(time, 2.4, ambientTemperature[i]))
                changeDictionaryDict['T']['boundaryField']['container']['h'] = [self.heattransfer_coefficient(time, 2.4, ambientTemperature[i])]

            # Update ambient temperature
            changeDictionaryDict['T']['boundaryField']['container']['Ta'] = [ambientTemperature[i]]
            changeDictionaryDict.writeFile()
            
            # Update endTime of the simulation
            controlDict['endTime'] = controlDict['endTime'] + 3600
            controlDict.writeFile()
            
            # Execute solver
            os.system(os.path.join(self.name,"Run"))

            #File management of log files
            # original = os.path.join(self.name,"log.chtMultiRegionFoam")
            # target = os.path.join(self.name,"log.chtMultiRegionFoam") + '_' + str(i))
            # shutil.copyfile(original, target)
            # os.remvoe(original)
            os.system('cp ' + os.path.join(self.name,"log.chtMultiRegionFoam") + ' ' + os.path.join(self.name,"log.chtMultiRegionFoam") + '_' + str(i))
            os.system('rm ' + os.path.join(self.name,"log.chtMultiRegionFoam"))

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

        # Find all regions by direcotries in postProcessing, PyFoam folder is no regionS
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


        


