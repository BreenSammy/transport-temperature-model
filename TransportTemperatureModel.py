import os

import numpy as np
import pandas as pd

import modules.case as case
from modules.case import Case
import modules.transport as transport


#transport_path = os.path.join('transports', 'grandlgruber', 'grandlgruber.json')
# transport_path = os.path.join('transports', 'Berlin-Garching', 'Berlin-Garching.json')
# transport_path = os.path.join('transports', 'fairWeather_container_template', 'fairWeather_container_template.json')
transport_path = os.path.join('transports', 'schenker_A', 'schenker_A.json')
# case_path = os.path.join('transports', 'Berlin-Garching', 'case')
#case_path = os.path.join('transports', 'grandlgruber', 'case')

transport1 = transport.from_json(transport_path)

transport1.save()

case = case.setup(transport1, initial_temperature = 298.15, cpucores = 20, force_clone = True)

case.run()

case.reconstruct()

case.postprocess()

# case = Case(case_path)
# case.plot()
case.probe_freight('battery0_0')

# # # case.probe([1.6505, -0.905, 0.105], 'airInside', clear = True)

case.pack_solution(logs = False)


