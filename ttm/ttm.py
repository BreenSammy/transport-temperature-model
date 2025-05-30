#!/usr/bin/env python3

import argparse
import glob
import os
import shutil

import ttm.transport as tp
from ttm.case import Case
import ttm.visualization as visualization

parser = argparse.ArgumentParser(usage='%(prog)s [options]')
# Options
parser.add_argument(
    "--transport", "-t", 
    help="Alternative transport directory (instead of cwd)", 
    metavar="<dir>", 
    default=os.getcwd()
    )
parser.add_argument(
    "--clone", "-c",
    help="Force to clone from template and overwrite case",
    action="store_true"
    )
parser.add_argument(
    "--cpucores", 
    type=int, 
    help="Set the number of cpu cores used for the simulation", 
    metavar="cpucount"
    )
parser.add_argument(
    "--reconstruct", "-r", 
    help="Reconstruct the decomposed case", 
    action="store_true"
    )
parser.add_argument(
    "--postprocess", 
    help="Execute postprocess utility of the simulation case", 
    action="store_true"
    )
parser.add_argument(
    "--plot", 
    help="""Plot postprocess results. 
            Use arguments to probe freight regions. 
            Use argument all to probe all freight regions""", 
    nargs="*", 
    metavar="freightregion"
    )
parser.add_argument(
    "--probe", 
    help="Read temperature from a location '(x y z)'", 
    metavar=("region", "location"), 
    nargs='+')
parser.add_argument(
    "--probefreight", 
    help="Read temperature from one freight region for each freight element", 
    metavar="region"
    )
parser.add_argument(
    "--pack", 
    help="Pack the case as a compressed file", 
    action="store_true"
    )
parser.add_argument(
    "--arrival", 
    help="Simulate the heattransfer after transport", 
    action="store_true"
    )
parser.add_argument(
    "--weather", "-w", 
    help="Reload weatherdata", 
    action="store_true"
    )
parser.add_argument(
    "--savetimes", "-s", 
    help="Save timedirectories", 
    action="store_true"
    )

def main():
    args = parser.parse_args()

    # Get the path of the transport directory, default cwd
    transportpath = args.transport

    # Read transport from json and create transport instance
    transport = tp.from_json(os.path.join(transportpath, 'transport.json'))
    # Reload weatherdata from NOAA database
    if args.weather:
        transport.weatherdata = transport.get_weatherdata()

    # Setup the case for the simulation 
    casepath = os.path.join(transportpath, 'case')
    templatecasepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templatecase'
        )

    if not os.path.exists(casepath) or args.clone:
        # Delete all contents of postProcessing and plots
        files = glob.glob(transport._postprocesspath + '/**/*.*', recursive=True)
        files += glob.glob(transport._plotspath + '/**/*.*', recursive=True)
        for f in files:
            os.remove(f)
        if os.path.exists(casepath):
            shutil.rmtree(casepath)
        templatecase = Case(templatecasepath)
        transportcase = templatecase.cloneCase(casepath)
    else:
        transportcase = Case(casepath)

    if args.cpucores:
        transportcase.change_number_cpucores(args.cpucores)

    # Those functions should only be executed, if the mesh does not already exist
    if not transportcase.processorDirs():
        transportcase.change_transporttype(transport.type)
        transportcase.change_initial_temperature(transport.initial_temperature)
        transportcase.load_cargo(transport.cargo)
        transportcase.create_mesh()
    else:
        print('Mesh already exists')

    # Set purge write switch if timedirectories should not be saved 
    if args.savetimes == False:
        transportcase.set_purge_write()

    # Execute the OpenFOAM solver
    if transport.type == 'car':
        transportcase.switch_to_car()
        transportcase.run(borderregion = 'battery0_0')
    else:
        transportcase.run()

    # Simulate arrival
    if args.arrival:
        transportcase.simulate_arrival(transport.arrival_temperature)

    # Postprocess the simulation
    if args.probe:
        if args.probe[0] == 'file':
            filepath = os.path.join(transportpath, 'probe_locations.csv')
            transportcase.probe_from_file(filepath)
        else:
            region = args.probe[0]
            location = [float(i) for i in args.probe[1][1:-1].split(' ')]
            transportcase.probe(region, location=location, clear=False)

    if args.probefreight:
        # print(args.probefreight)
        transportcase.probe_freight(args.probefreight)

    postprocessed_regions = [
        os.path.splitext(region)[0] for region in os.listdir(transport._postprocesspath_temperature)
        ]
        
    # Postprocess if not all regions have been postprocessed or if flag is set
    if sorted(postprocessed_regions) !=  sorted(transportcase.regions()) or args.postprocess:
        print('Running postprocess on transport')
        transportcase.postprocess()

    # if (transportcase.latesttime() - transportcase.duration()) > 1000:
    #     print('Running postprocess on arrival')
    #     transportcase.postprocess(arrival=True)

    # Plot results
    plots_content = os.listdir(transport._plotspath)
    if 'plot.jpg' not in plots_content or args.plot:
        print('Plotting simulation results')
        if args.plot != None:
            if 'all' in args.plot:
                args.plot = transportcase.cargo_regions()
            [transportcase.probe_freight(region) for region in args.plot]
        visualization.plot(transport)

    visualization.transport(transport)

    if args.reconstruct:
        transportcase.reconstruct()
    if args.pack:
        transportcase.pack(logs = False)