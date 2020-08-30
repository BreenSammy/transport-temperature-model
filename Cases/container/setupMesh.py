from pathlib import Path
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector
# from PyFoam.Basics.DataStructures

import pandas as pd
import numpy as np

import os
from subprocess import call

# class Battery:
#     def __init__(self, position):

class Pallet:
    """Class to describe a pallet full of packages."""
    def __init__(self, STL: str, number_packages: int, position: np.array, orientation: np.array):
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
        return "'(" + str(vector[0]) + ' ' + str(vector[1]) + ' ' + str(vector[2]) + ")'"
    
    def move_STL(self, case, target):
        """Move the STL to the right position in the carrier."""

        os.system(
            'surfaceTransformPoints -rollPitchYaw ' + self.vector_to_string(self.orientation) + " " + 
            os.path.join(case.name,"constant", "triSurface", self.STL) + " " + 
            os.path.join(case.name,"constant", "triSurface", target)
            )

        os.system(
            'surfaceTransformPoints -translate ' + self.vector_to_string(self.position) + " " + 
            os.path.join(case.name,"constant", "triSurface", target) + " " + 
            os.path.join(case.name,"constant", "triSurface", target)
            )

        self.STL = target



templateCase = SolutionDirectory("container_template", archive=None, paraviewLink=False)

pallets = [
    #Pallet('pallet4x4.stl', 8, np.array([0.44, -0.54, 0.144]), np.array([0, 0, 90])),
    #Pallet('pallet4x4.stl', 8, np.array([1.28, -0.54, 0.144]), np.array([0, 0, 90])),
    #Pallet('pallet4x4.stl', 8, np.array([2.12, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet4x4.stl', 8, np.array([2.96, -0.54, 0.144]), np.array([0, 0, 90])),
    #Pallet('pallet4x4.stl', 8, np.array([3.80, -0.54, 0.144]), np.array([0, 0, 90])),
    #Pallet('pallet4x4.stl', 8, np.array([4.64, -0.54, 0.144]), np.array([0, 0, 90])),
    #Pallet('pallet4x4.stl', 8, np.array([5.48, -0.54, 0.144]), np.array([0, 0, 90]))
    ]

case = templateCase.cloneCase("container_0")

snappyHexMeshDict = ParsedParameterFile(os.path.join(case.name,"system", "snappyHexMeshDict"))

targetSTL = 'pallet_{}.stl'
refinementSurfacesLevel = [5,5]

#airInside_changeDictionaryDict = ParsedParameterFile(os.path.join(case.name,'system','airInside','changeDictionaryDict'))
regionProperties = ParsedParameterFile(os.path.join(case.name,'constant','regionProperties'))



for i in range(len(pallets)):
    geometryName = targetSTL.format(i).split('.', 1)[0]
    #os.system(cmd + " " + pallets[i].translate_string() + " " + os.path.join(case.name,"constant", "triSurface", sourceSTL) + " " + os.path.join(case.name,"constant", "triSurface", targetSTL.format(i)))
    # Move the STL file to the right position in the carrier
    pallets[i].move_STL(case, targetSTL.format(i))

    #Creating the snappyHexMeshDict for the carrier
    snappyHexMeshDict['geometry'].__setitem__(targetSTL.format(i), {'type': 'triSurfaceMesh', 'name': geometryName})
    snappyHexMeshDict['castellatedMeshControls']['refinementSurfaces'].__setitem__(geometryName, {'level': refinementSurfacesLevel})

    for j in range(len(pallets[i].package_positions)):

        battery_name =  "battery" + str(i)+ '_' + str(j)
        battery_system_path = os.path.join(case.name,"system", battery_name)

        snappyHexMeshDict['castellatedMeshControls']['locationsInMesh'].append([pallets[i].package_positions[j], battery_name])

        os.system('cp -r ' + os.path.join(case.name,"system", "battery_template") + " " + battery_system_path)
        os.system('cp -r ' + os.path.join(case.name,"constant", "battery_template") + " " + os.path.join(case.name,"constant", battery_name))
        os.system('cp -r ' + os.path.join(case.name,"0.org", "battery_template") + " " + os.path.join(case.name,"0.org", battery_name))

        battery_changeDictionaryDict = ParsedParameterFile(os.path.join(battery_system_path,'changeDictionaryDict'))
        battery_changeDictionaryDict['T']['boundaryField'].__setitem__(
            battery_name + '_to_airInside', 
            battery_changeDictionaryDict['T']['boundaryField'].__getitem__('battery0_0_to_airInside')
            )
        battery_changeDictionaryDict['T']['boundaryField'].__delitem__('battery0_0_to_airInside')
        battery_changeDictionaryDict.writeFile()

        #Names of the solid regions are in third entry of the list regions, adding batteries
        regionProperties['regions'][3].append(battery_name)

        #changeDictionaryDict.closeFile()    
    #print(changeDictionaryDict['T']['boundaryField'].__getitem__('battery0_0_to_airInside'))
    #print(snappyHexMeshDict['castellatedMeshControls']['locationsInMesh'])




    #path_snappyHexMeshDict = Path("system/snappyHexMeshDict")

    # snappyHexMeshDict = ParsedParameterFile(path_snappyHexMeshDict)
    # snappyHexMeshDict['geometry'].__setitem__([targetSTL.format(i), None])
    # print(snappyHexMeshDict['geometry'])
    #ParsedParameterFile(path_snappyHexMeshDict)["geometry"].__setitem__(['boxes01.stl'], None)

regionProperties.writeFile()
snappyHexMeshDict.writeFile()

# print(type(path_snappyHexMeshDict))
# print(path_snappyHexMeshDict)

# cell_coordinates = ParsedParameterFile(path_cell)["internalField"].val

# path_temperature = Path("100/batteries/T")

# T = ParsedParameterFile(path_temperature)["internalField"].val

# df = pd.DataFrame(
#     list(zip(T,cell_coordinates)),
#     columns = ['T','Coordinates']
# )

# ParsedParameterFile(path_snappyHexMeshDict)["geometry"].__setitem__(['boxes01.stl'], None)

# print(ParsedParameterFile(path_snappyHexMeshDict)["geometry"].__setitem__(['boxes01.stl'], None))

# snappyDict = ParsedParameterFile(path_snappyHexMeshDict)["geometry"].__deepcopy__(ParsedParameterFile(path_snappyHexMeshDict)["geometry"])

#snappyDict = ParsedParameterFile(path_snappyHexMeshDict)

#snappyDict = ParsedParameterFile(os.path.join(case.name,"system", "snappyHexMeshDict"))

#snappyDict['boxes01.stl'].__setitem__('test', 'test')

#print(snappyDict["geometry"]['out.stl'])
# print(ParsedParameterFile(path_snappyHexMeshDict)["geometry"].__deepcopy__(ParsedParameterFile(path_snappyHexMeshDict)["geometry"]))