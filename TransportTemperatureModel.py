from datetime import date, datetime
import json
import os

import numpy as np
import pandas as pd
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

import modules.case as case
from modules.case import Case
from modules.cargo import Pallet
import modules.weather.weather as weather
from modules.route import Stop, RouteGPX
import modules.transport as transport
from modules.transport import Transport

# pallets = [
#     #Pallet('pallet1x4.stl', 4, np.array([0.5399, -0.54, 0.144]), np.array([0, 0, 90])),
#     Pallet('pallet_0', 'pallet2x4.stl', [1.3601, -0.54, 0.144], [0, 0, 90]),
#     Pallet('pallet_1', 'pallet2x4.stl' , [2.2001, -0.54, 0.144], [0, 0, 90]),
#     # Pallet('pallet2x4.stl', 8, np.array([3.0401, -0.54, 0.144]), np.array([0, 0, 90])),
#     # Pallet('pallet3x4.stl', 12, np.array([3.8801, -0.54, 0.144]), np.array([0, 0, 90])),
#     # Pallet('pallet2x4.stl', 8, np.array([4.7201, -0.54, 0.144]), np.array([0, 0, 90])),
#     # Pallet('pallet2x4.stl', 8, np.array([5.5601, -0.54, 0.144]), np.array([0, 0, 90])),
#     # Pallet('pallet3x4.stl', 12, np.array([0.8801, 0.5301, 0.144]), np.array([0, 0, 0])),
#     # Pallet('pallet3x4.stl', 12, np.array([2.3201, 0.5301, 0.144]), np.array([0, 0, 0])),
#     # Pallet('pallet3x4.stl', 12, np.array([3.7601, 0.5301, 0.144]), np.array([0, 0, 0])),
#     # Pallet('pallet3x4.stl', 12, np.array([5.2001, 0.5301, 0.144]), np.array([0, 0, 0])),
#     ]

#transport_path = os.path.join('transports', 'grandlgruber', 'grandlgruber.json')
transport_path = os.path.join('transports', 'Berlin-Garching', 'Berlin-Garching.json')
#case_path = os.path.join('transports', 'Berlin-Garching', 'case')
case_path = os.path.join('transports', 'grandlgruber', 'case')

with open(transport_path) as json_file:
    transport1 = transport.from_json(json_file, reread_temperature = True)

transport1.save()

case = case.setup(transport1, force_clone = True)
case.run()

#case = Case(case_path)
case.reconstruct()
#case.probe([0, 0, 0])

# gpx_path = os.path.join('transports', 'grandlgruber', 'grandlgruber.gpx')

# route = RouteGPX(gpx_path)

#print(route.dataframe_full)



