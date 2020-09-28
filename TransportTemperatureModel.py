import os

import numpy as np
import pandas as pd

import modules.case as case
from modules.case import Case

import modules.transport as transport


#transport_path = os.path.join('transports', 'grandlgruber', 'grandlgruber.json')
transport_path = os.path.join('transports', 'Berlin-Garching', 'Berlin-Garching.json')
case_path = os.path.join('transports', 'Berlin-Garching', 'case')
#case_path = os.path.join('transports', 'grandlgruber', 'case')

# with open(transport_path) as json_file:
#     transport1 = transport.from_json(json_file, reread_temperature = True)

# transport1.save()

# case = case.setup(transport1, initial_temperature = 293, force_clone = False)

# case.run()

case = Case(case_path)
case.probe( [2, 1, 1], 'airInside', time = 3605)
#case.reconstruct()
#case.probe([0, 0, 0])

# gpx_path = os.path.join('transports', 'grandlgruber', 'grandlgruber.gpx')

# route = RouteGPX(gpx_path)

#print(route.dataframe_full)



