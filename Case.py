import os

import numpy as np
import pandas as pd

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector

import modules.convection as convection

class Case(SolutionDirectory):
    def __init__(self, name, archive=None, paraviewLink=False):
        SolutionDirectory.__init__(self, name, archive=None, paraviewLink=False)

        # Add scripts to control simulation to cloneCase
        self.addToClone('Allrun.pre')
        self.addToClone('Run')
    
    def setup_case(self, cargo):
        """Loads the carrier with cargo. New Regions for cargo 
        are added to snappyHexMeshDict and regionProperties"""
        refinementSurfacesLevel = [3,3]

        # Files that need to be modified
        regionProperties = ParsedParameterFile(os.path.join(self.constantDir(),'regionProperties'))
        snappyHexMeshDict = ParsedParameterFile(os.path.join(self.systemDir(), "snappyHexMeshDict"))

        for i in range(len(cargo)):
            cargo[i].move_STL(self, cargo[i].name + '.stl')

            # Adding current cargo to the snappyHexMeshDict
            snappyHexMeshDict['geometry'].__setitem__(cargo[i].name + '.stl', {'type': 'triSurfaceMesh', 'name': cargo[i].name})
            snappyHexMeshDict['castellatedMeshControls']['refinementSurfaces'].__setitem__(cargo[i].name, {'level': refinementSurfacesLevel})

            for j in range(len(cargo[i].package_positions)):
                battery_name = "battery" + str(i) + '_' + str(j)
                battery_system_path = os.path.join(self.systemDir(), battery_name)

                snappyHexMeshDict['castellatedMeshControls']['locationsInMesh'].append(
                    [cargo[i].package_positions[j], battery_name])

                os.system('cp -r ' + os.path.join(self.systemDir(), "battery_template") + " " + battery_system_path)
                os.system('cp -r ' + os.path.join(self.constantDir(), "battery_template") + " " + os.path.join(self.name, "constant", battery_name))
                os.system('cp -r ' + os.path.join(self.name, "0.org", "battery_template") + " " + os.path.join(self.name, "0.org", battery_name))

                battery_changeDictionaryDict = ParsedParameterFile(os.path.join(battery_system_path, 'changeDictionaryDict'))
                battery_changeDictionaryDict['T']['boundaryField'].__setitem__(
                    battery_name + '_to_airInside',
                    battery_changeDictionaryDict['T']['boundaryField'].__getitem__(
                    'battery0_0_to_airInside'))
                battery_changeDictionaryDict['T']['boundaryField'].__delitem__(
                    'battery0_0_to_airInside')
                battery_changeDictionaryDict.writeFile()

                #Names of the solid regions are in third entry of the list regions, adding batteries
                regionProperties['regions'][3].append(battery_name)

        regionProperties.writeFile()
        snappyHexMeshDict.writeFile()

    # def remove_cargo(self):


    def create_mesh(self):
        os.system(os.path.join(self.name,"Allrun.pre"))

    def heattransfer_coefficient(self, time, L, T_U):
        # Value for current time is saved in folder for last time
        time = time - 3600
        path_averageTemperature = os.path.join(
            self.name,'postProcessing','airInside','temperature_right',str(time),'surfaceFieldValue.dat'
            )    
        df_patch_temperature = pd.read_table(path_averageTemperature, sep="\s+", header=4, usecols = [0,1], names = ['time', 'T'])
        T_W = df_patch_temperature['T'].iloc[-1]
        return convection.coeff_natural(L, T_W, T_U)

    def run(self, ambientTemperature):

        changeDictionaryDict = ParsedParameterFile(os.path.join(self.systemDir(), "airInside", "changeDictionaryDict"))
        controlDict = ParsedParameterFile(os.path.join(self.systemDir(), "controlDict"))
        
        for i in range(len(ambientTemperature)):
            
            time = controlDict['endTime']
            print(time)
            if time != 0:
                print(self.heattransfer_coefficient(time, 2.4, ambientTemperature[i]))
                changeDictionaryDict['T']['boundaryField']['container']['h'] = [self.heattransfer_coefficient(time, 2.4, ambientTemperature[i])]


            changeDictionaryDict['T']['boundaryField']['container']['Ta'] = [ambientTemperature[i]]
            changeDictionaryDict.writeFile()
            
            controlDict['endTime'] = controlDict['endTime'] + 3600
            controlDict.writeFile()
            
            os.system(os.path.join(self.name,"Run"))

            os.system('cp ' + os.path.join(self.name,"log.chtMultiRegionFoam") + ' ' + os.path.join(self.name,"log.chtMultiRegionFoam") + '_' + str(i))
            os.system('rm ' + os.path.join(self.name,"log.chtMultiRegionFoam"))




class Pallet:
    """Class to describe a pallet full of packages."""
    def __init__(self, name: str, STL: str, number_packages: int, position: np.array, orientation: np.array):
        self.name = name
        self.STL = STL
        self.number_packages = number_packages
        self.position = position
        self.orientation = orientation
        position_vector = Vector(position[0], position[1], position[2])
        
        # Save positions of seperate packages for locationsInMesh in snappyHexMeshDict
        self.package_positions = []
        for i in range(int(self.number_packages/4)):
            z_coordinate = self.position[2] + 0.15505 + 0.400*i
            self.package_positions.extend([
                position_vector.__add__(Vector(0.201, 0.201, z_coordinate)), position_vector.__add__(Vector(0.201, -0.201, z_coordinate)),
                position_vector.__add__(Vector(-0.201, -0.201, z_coordinate)), position_vector.__add__(Vector(-0.201, 0.201, z_coordinate)),
            ])

    def vector_to_string(self, vector):
        """Transform a vector with three entries into a string for terminal commands"""
        return "'(" + str(vector[0]) + ' ' + str(vector[1]) + ' ' + str(vector[2]) + ")'"
    
    def move_STL(self, case, target):
        """Move the STL to the right position in the carrier."""

        # Copy STL form template STL and bring it in the right orientation
        os.system(
            'surfaceTransformPoints -rollPitchYaw ' + self.vector_to_string(self.orientation) + " " + 
            os.path.join(case.constantDir(), "triSurface", self.STL) + " " + 
            os.path.join(case.constantDir(), "triSurface", target)
            )

        # Move STL to its position
        os.system(
            'surfaceTransformPoints -translate ' + self.vector_to_string(self.position) + " " + 
            os.path.join(case.constantDir(), "triSurface", target) + " " + 
            os.path.join(case.constantDir(), "triSurface", target)
            )
        self.STL = target
