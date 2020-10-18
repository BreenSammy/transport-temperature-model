#!/usr/bin/env python3

import argparse
import os

import modules.transport as transport
from modules.case import Case

parser = argparse.ArgumentParser(usage='%(prog)s [options]')

parser.add_argument("--transport", "-t", help="Alternative transport directory (instead of cwd)", metavar="<dir>", default=os.getcwd())
parser.add_argument("--clone", "-c", help="Force to clone from template and overwrite case", action="store_true")
parser.add_argument("--cpucores", type=int, help="Set the number of cpu cores used for the simulation", metavar="cpucount")
parser.add_argument("--reconstruct", help="Reconstruct the decomposed case", action="store_true")
parser.add_argument("--probe", help="Read temperature from freight", action="store_true")
parser.add_argument("--pack", help="Pack the case as a compressed file", action="store_true")
parser.add_argument("--arrival", help="Simulate the heattransfer after transport", action="store_true")

args = parser.parse_args()

# Get the path of the transport directory, default cwd
transportpath = args.transport

# Read transport from json and create transport instance
transport = transport.from_json(os.path.join(transportpath, 'transport.json'))

# Setup the case for the simulation 
casepath = os.path.join(transportpath, 'case')
templatecasepath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'cases', 'container', 'container_template'
    )

if not os.path.exists(casepath) or args.clone:
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

# Execute the OpenFOAM solver
transportcase.run()

if args.pack:
    transportcase.pack()

# Postprocess the simulation
if args.reconstruct:
    transportcase.reconstruct()
if args.arrival:
    transportcase.simulate_arrival()

transportcase.postprocess()
transportcase.plot(probes = ['battery0_0', 'battery0_1'], tikz = True)