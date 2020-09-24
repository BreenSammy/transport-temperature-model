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
from modules.route.route import Stop
import modules.transport as transport
from modules.transport import Transport


#templateCase = Case(os.path.join('Cases', 'container', 'container_template_new'))

ambientTemperature = np.array([
    285, 286, 287, 289, 290, 292, 294, 295, 296, 296, 295, 293,
    292, 290, 289, 298, 287, 286, 285, 284, 283, 281, 280, 281,
    285, 286, 287, 289, 290, 292, 294, 295, 296, 296, 295, 293,
    292, 290, 289, 298, 287, 286, 285, 284, 283, 281, 280, 281, 
    285, 286, 287, 289, 290, 292, 294, 295, 296, 296, 295, 293,
    292, 290, 289, 298, 287, 286, 285, 284, 283, 281, 280, 281, 
    285, 286, 287, 289, 290, 292, 294, 295, 296, 296, 295, 293,
    292, 290, 289, 298, 287, 286, 285, 284, 283, 281, 280, 281 
    ])

ambientTemperature = np.array([
    285, 286, 287
    ])

pallets = [
    #Pallet('pallet1x4.stl', 4, np.array([0.5399, -0.54, 0.144]), np.array([0, 0, 90])),
    Pallet('pallet_0', 'pallet2x4.stl', [1.3601, -0.54, 0.144], [0, 0, 90]),
    Pallet('pallet_1', 'pallet2x4.stl' , [2.2001, -0.54, 0.144], [0, 0, 90]),
    # Pallet('pallet2x4.stl', 8, np.array([3.0401, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet3x4.stl', 12, np.array([3.8801, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet2x4.stl', 8, np.array([4.7201, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet2x4.stl', 8, np.array([5.5601, -0.54, 0.144]), np.array([0, 0, 90])),
    # Pallet('pallet3x4.stl', 12, np.array([0.8801, 0.5301, 0.144]), np.array([0, 0, 0])),
    # Pallet('pallet3x4.stl', 12, np.array([2.3201, 0.5301, 0.144]), np.array([0, 0, 0])),
    # Pallet('pallet3x4.stl', 12, np.array([3.7601, 0.5301, 0.144]), np.array([0, 0, 0])),
    # Pallet('pallet3x4.stl', 12, np.array([5.2001, 0.5301, 0.144]), np.array([0, 0, 0])),
    ]

#case = Case('testing')
# case = templateCase.cloneCase("testing")
# case.load_cargo(pallets)
# case.create_mesh()
# case.run(ambientTemperature)
# case.reconstruct()



#print(case.name)

# case = Case('testing_2')
# #case.load_cargo(pallets)

# # controlDict = ParsedParameterFile(os.path.join(case.systemDir(), "controlDict"))

# # case.create_function_objects('battery0_2', controlDict)

# # controlDict.writeFile()
#case.postprocess()


# stop_lat = [51.38503, 50.407]
# stop_lon = [12.18273, 11.77477]
# stop_start = [datetime(2019, 3, 2, 7, 15), datetime(2019, 3, 2, 9, 35)]
# stop_end = [datetime(2019, 3, 2, 8, 15), datetime(2019, 3, 2, 9, 35)]

# d = {'Start': stop_start, 'End': stop_end, 'Lat': stop_lat, 'Lon': stop_lon}

# stops = pd.DataFrame(data = d)

# stops = [
#     Stop(
#         datetime(2019, 3, 2, 7, 15),
#         datetime(2019, 3, 2, 8, 15),
#         51.38503,
#         12.18273
#     ),
#     Stop(
#         datetime(2019, 3, 2, 9, 35),
#         datetime(2019, 3, 2, 9, 35),
#         50.407,
#         11.77477
#     )
# ]

# rows =  [item.to_dict() for item in stops]  



# start = datetime(2019, 3, 2, 5, 23)
# end = datetime(2019, 3, 2, 14, 30)

# Transport_berlin_garching = Transport(start, end, pallets,'Berlin-Garching.csv', stops = stops)

# Transport_berlin_garching.save('Berlin-Garching')

# Transport_berlin_garching.to_csv('B-G.csv')

# print(Transport_berlin_garching.__dict__)


# #datetime = datetime(2018, 3, 2, 5)
start = datetime(2019, 3, 2, 5)
# end = datetime(2019, 3, 5, 5)

# #print(datetime)

# #Weateher = weather.Weather()

# #weather.hello()

# temperature = weather.temperature(start, 52, 5)
# temperature = weather.data(start, end, 44, 12)

# print(temperature)


transport_path = os.path.join('transports', 'Berlin-Garching', 'Berlin-Garching.json')
case_path = os.path.join('transports', 'Berlin-Garching', 'case')

with open(transport_path) as json_file:
    transport1 = transport.from_json(json_file)

transport1.save()

case = case.setup(transport1)

case.run()

# case = Case(case_path)
case.reconstruct()

# transport1.save('Berlin-Garching')

