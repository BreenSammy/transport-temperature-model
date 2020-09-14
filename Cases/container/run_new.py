import os

import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector


templateCase = SolutionDirectory("container_2", archive=None, paraviewLink=False)


case = templateCase.cloneCase("container_22")


os.system('cp ' + os.path.join(templateCase.name,"Allrun.pre") + " " + case.name)
os.system('cp ' + os.path.join(templateCase.name,"Run") + " " + case.name)

changeDictionaryDict = ParsedParameterFile(os.path.join(case.name,"system", "airInside", "changeDictionaryDict"))
controlDict = ParsedParameterFile(os.path.join(case.name,"system", "controlDict"))


ambientTemperature = np.array([
    285, 286, 287, 289, 290, 292, 294, 295, 296, 296, 295, 293,
    292, 290, 289, 298, 287, 286, 285, 284, 283, 281, 280, 281 
    ])

print(changeDictionaryDict['T']['boundaryField']['container']['Ta'])
os.system(os.path.join(case.name,"Allrun.pre"))

for i in range(24):
    changeDictionaryDict['T']['boundaryField']['container']['Ta'] = [ambientTemperature[i]]
    changeDictionaryDict.writeFile()
    
    controlDict['endTime'] = (i+1)*3600
    controlDict.writeFile()
    
    os.system('rm ' + os.path.join(case.name,"log.changeDictionary.airInside"))

    os.system(os.path.join(case.name,"Run"))

    os.system('cp ' + os.path.join(case.name,"log.chtMultiRegionFoam") + ' ' + os.path.join(case.name,"log.chtMultiRegionFoam") + '_' + str(i))
    os.system('rm ' + os.path.join(case.name,"log.chtMultiRegionFoam"))


