import os

from Case import Case
from modules.Cargo import Pallet
import numpy as np
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


templateCase = Case(os.path.join('Cases', 'container', 'container_template_new'))

ambientTemperature = np.array([
    285, 286, 287, 289, 290, 292, 294, 295, 296, 296, 295, 293,
    292, 290, 289, 298, 287, 286, 285, 284, 283, 281, 280, 281 
    ])

# ambientTemperature = np.array([
#     285, 286, 287
#     ])

pallets = [
    #Pallet('pallet1x4.stl', 4, np.array([0.5399, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet_0', 'pallet2x4.stl', 8, np.array([1.3601, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet2x4.stl', 8, np.array([2.2001, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet2x4.stl', 8, np.array([3.0401, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet3x4.stl', 12, np.array([3.8801, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet2x4.stl', 8, np.array([4.7201, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet2x4.stl', 8, np.array([5.5601, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet3x4.stl', 12, np.array([0.8801, 0.5301, 0.144]), np.array([0, 0, 0])),
    # Pallet('pallet3x4.stl', 12, np.array([2.3201, 0.5301, 0.144]), np.array([0, 0, 0])),
    # Pallet('pallet3x4.stl', 12, np.array([3.7601, 0.5301, 0.144]), np.array([0, 0, 0])),
    # Pallet('pallet3x4.stl', 12, np.array([5.2001, 0.5301, 0.144]), np.array([0, 0, 0])),
    ]

# case = templateCase.cloneCase("testing_2")
# case.load_cargo(pallets)
# case.create_mesh()
# case.run(ambientTemperature)
# case.reconstruct()

# case.setup_case(pallets)

#print(case.name)

case = Case('testing_2')

# controlDict = ParsedParameterFile(os.path.join(case.systemDir(), "controlDict"))

# case.create_function_objects('battery0_2', controlDict)

# controlDict.writeFile()
case.post_process()
