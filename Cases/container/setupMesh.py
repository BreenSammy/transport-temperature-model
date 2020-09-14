import os

import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector


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
        """Transform a vector with three entries into a string for terminal commands"""
        return "'(" + str(vector[0]) + ' ' + str(vector[1]) + ' ' + str(vector[2]) + ")'"
    
    def move_STL(self, case, target):
        """Move the STL to the right position in the carrier."""

        # Copy STL form template STL and bring it in the right orientation
        os.system(
            'surfaceTransformPoints -rollPitchYaw ' + self.vector_to_string(self.orientation) + " " + 
            os.path.join(case.name,"constant", "triSurface", self.STL) + " " + 
            os.path.join(case.name,"constant", "triSurface", target)
            )

        # Move STL to its position
        os.system(
            'surfaceTransformPoints -translate ' + self.vector_to_string(self.position) + " " + 
            os.path.join(case.name,"constant", "triSurface", target) + " " + 
            os.path.join(case.name,"constant", "triSurface", target)
            )

        self.STL = target



templateCase = SolutionDirectory("container_template_new", archive=None, paraviewLink=False)

pallets = [
    Pallet('pallet1x4.stl', 4, np.array([0.5399, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet2x4.stl', 8, np.array([1.3601, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet2x4.stl', 8, np.array([2.2001, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet2x4.stl', 8, np.array([3.0401, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet3x4.stl', 12, np.array([3.8801, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet2x4.stl', 8, np.array([4.7201, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet2x4.stl', 8, np.array([5.5601, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet3x4.stl', 12, np.array([0.8801, 0.5301, 0.144]), np.array([0, 0, 0])),
    Pallet('pallet3x4.stl', 12, np.array([2.3201, 0.5301, 0.144]), np.array([0, 0, 0])),
    Pallet('pallet3x4.stl', 12, np.array([3.7601, 0.5301, 0.144]), np.array([0, 0, 0])),
    Pallet('pallet3x4.stl', 12, np.array([5.2001, 0.5301, 0.144]), np.array([0, 0, 0])),
    ]

case = templateCase.cloneCase("container_2")

os.system('cp ' + os.path.join(templateCase.name,"Allrun.pre") + " " + case.name)
os.system('cp ' + os.path.join(templateCase.name,"Run") + " " + case.name)

snappyHexMeshDict = ParsedParameterFile(os.path.join(case.name,"system", "snappyHexMeshDict"))

targetSTL = 'pallet_{}.stl'
refinementSurfacesLevel = [4,4]

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