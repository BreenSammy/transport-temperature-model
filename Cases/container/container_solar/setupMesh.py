from pathlib import Path
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
# from PyFoam.Basics.DataStructures

import pandas as pd
import numpy as np


path_snappyHexMeshDict = Path("system/snappyHexMeshDict")

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

snappyDict = ParsedParameterFile(path_snappyHexMeshDict)["geometry"]

snappyDict['boxes01.stl'].__setitem__('test', 'test')

print(snappyDict)
# print(ParsedParameterFile(path_snappyHexMeshDict)["geometry"].__deepcopy__(ParsedParameterFile(path_snappyHexMeshDict)["geometry"]))