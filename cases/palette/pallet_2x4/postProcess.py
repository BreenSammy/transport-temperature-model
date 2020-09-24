import os

import numpy as np

from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.Basics.DataStructures import Vector

os.system('cp system/singleGraphx system/singleGraph')
os.system('./postProcess')

os.system('cp postProcessing/singleGraph/data.csv postProcessing/plotx.csv')

os.system('cp system/singleGraphz system/singleGraph')
os.system('./postProcess')

os.system('cp postProcessing/singleGraph/data.csv postProcessing/plotz.csv')

os.system('rm system/singleGraph')