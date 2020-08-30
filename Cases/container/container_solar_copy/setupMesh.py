from pathlib import Path
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

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
print('Hello World')
