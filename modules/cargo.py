import copy
from math import floor, sqrt
import os

import numpy as np
from PyFoam.Basics.DataStructures import Vector
from scipy.spatial.transform import Rotation 

# Number of individual packages (regions) in the stl
# (number of layers, packages per layer) 
NUMBER_PACKAGES = {
    'pallet1x4.stl': (1, 4),
    'pallet2x4.stl': (2, 4),
    'pallet3x4.stl': (3, 4),
    'industrial_pallet1x1.stl': (1, 1),
    'industrial_pallet1x4.stl': (1, 4)
}

DIMENSIONS_PACKAGE = {
    'pallet1x4.stl': [0.6, 0.4, 0.4],
    'pallet2x4.stl': [0.6, 0.4, 0.4],
    'pallet3x4.stl': [0.6, 0.4, 0.4],
    'industrial_pallet1x1.stl': [1.2, 1, 0.4],
    'industrial_pallet1x4.stl': [0.6, 0.5, 0.4]
}

FREIGHTTYPES = {'cells', 'modules', 'packs'}
THERMAL_CAPACITY_PACKAGING = 1600
THERMAL_CONDUCTIVITY_PACKAGING = 0.053
DENSITY_PACKAGING = 132

class BatteryRegion:
    """Class to represent a battery region in OpenFOAM case"""
    def __init__(self, position, dimensions, freight):
        self.position = position
        self.dimensions = dimensions
        self.freight = freight
        self.thermal_conductivity_packaging = THERMAL_CONDUCTIVITY_PACKAGING

    def density(self):
        """Calculate the average density"""
        volume_region = np.prod(self.dimensions)
        volume_battery = np.prod(self.freight.dimensions) * np.prod(self.freight.elements_in_package(self.dimensions))
        volume_packaging = volume_region - volume_battery
        return volume_packaging / volume_region * DENSITY_PACKAGING + volume_battery / volume_region * self.freight.density()

    def packaging_thickness(self):
        """Calculate the thickness of the packaging"""
        dimension_freight = np.array(self.freight.elements_in_package(self.dimensions)) * np.array(self.freight.dimensions)
        return np.average(self.dimensions - dimension_freight)

    def thermal_capacity(self):
        """Calculate the average thermal capacity of the region"""
        volume_region = np.prod(self.dimensions)
        volume_battery = np.prod(self.freight.dimensions) * np.prod(self.freight.elements_in_package(self.dimensions))
        volume_packaging = volume_region - volume_battery
        return (
            ((volume_packaging * DENSITY_PACKAGING * THERMAL_CAPACITY_PACKAGING + 
             volume_battery * self.freight.density() * self.freight.thermalcapacity))
             / (volume_region * self.density())
            )

class Pallet:
    """Class to describe a pallet full of packages filled with batteries."""
    def __init__(self, templateSTL: str, position: list, orientation: list, freight):
        self.type = 'Pallet'
        self.templateSTL = templateSTL
        self.position = position
        self.orientation = orientation
        self.freight = freight
        self.battery_regions = self.get_battery_regions()

    def get_battery_regions(self):
        """Create all battery regions of the pallet"""
        # Get the dimensions of individual packages on the pallet and rotate according to the orientation
        rotation = Rotation.from_rotvec(np.array(self.orientation) * np.pi / 180)
        dimensions_package = DIMENSIONS_PACKAGE[self.templateSTL]
        dimensions_package = list(map(abs, rotation.apply(dimensions_package)))
        # Also rotate the dimensions of the freight and thermal conductivity
        self.freight.dimensions = list(map(abs, rotation.apply(self.freight.dimensions)))
        self.freight.thermalconductivity = list(map(abs, rotation.apply(self.freight.thermalconductivity)))

        #Get array of center points of each freightelement in one package
        points_freight_elements = self.freight.location_elements(dimensions_package)

        # Save positions of seperate packages for locationsInMesh in snappyHexMeshDict 
        number_packages = NUMBER_PACKAGES[self.templateSTL]

        # Get the center points of the first layer of battery regions on the pallet
        pallet_footprint = np.array(dimensions_package[0:2]) * sqrt(number_packages[1])
        x = np.linspace(-pallet_footprint[0]/2, pallet_footprint[0]/2, int(sqrt(number_packages[1]) * 2) + 1)[1::2]
        y = np.linspace(-pallet_footprint[1]/2, pallet_footprint[1]/2, int(sqrt(number_packages[1]) * 2) + 1)[1::2]
        battery_regions_positions =  np.vstack(np.meshgrid(x, y, dimensions_package[2]/2)).reshape(3,-1).T
        battery_regions_positions += np.array([self.position])

        layercounter = 0
        battery_regions = []
        # Iterate over layers of packages
        while layercounter < number_packages[0]:
            # Iterate over number of packages per layer
            for j in range(number_packages[1]):
                battery_region_position = copy.deepcopy(battery_regions_positions[j, :])
                self.freight.elements_positions = battery_region_position + points_freight_elements
                # Add battery region
                battery_regions.append(
                    BatteryRegion(battery_region_position, dimensions_package, self.freight)
                )  
            battery_regions_positions += np.array([0, 0, dimensions_package[2]])
            layercounter += 1

        return battery_regions

    def vector_to_string(self, vector):
        """Transform a vector with three entries into a string for terminal commands"""
        return "'(" + str(vector[0]) + ' ' + str(vector[1]) + ' ' + str(vector[2]) + ")'"
    
    def move_STL(self, case, target):
        """Move the STL to the right position in the carrier."""

        # Copy STL form template STL and bring it in the right orientation
        os.system(
            'surfaceTransformPoints -rollPitchYaw ' + self.vector_to_string(self.orientation) + " " + 
            os.path.join(case.constantDir(), "triSurface", self.templateSTL) + " " + 
            os.path.join(case.constantDir(), "triSurface", target) + '> {}/log.move_STL'.format(case.name) 
            )

        # Move STL to its position
        os.system(
            'surfaceTransformPoints -translate ' + self.vector_to_string(self.position) + " " + 
            os.path.join(case.constantDir(), "triSurface", target) + " " + 
            os.path.join(case.constantDir(), "triSurface", target) + '>> {}/log.move_STL'.format(case.name)
            )
        self.STL = target

    def freight_elements(self):
        dimensions_package = DIMENSIONS_PACKAGE[self.templateSTL]
        return [floor(dimensions_package[i] / self.freight.dimensions[i]) for i in range(3)]

    def to_dict(self):
        """Transform essential attributes of pallet to dict to save as json in Transport class"""
        return {
            'type': 'Pallet',
            'templateSTL': self.templateSTL,
            'position': self.position,
            'orientation': self.orientation, 
            'freight': self.freight.to_dict()
        }

def cargoDecoder(obj):
    freight = freightDecoder(obj['freight'])
    if obj['type'] == 'Pallet':
        return Pallet(obj['templateSTL'], obj['position'], obj['orientation'], freight)

class Freight:
    """Class to represent the shipped freight, e.g. battery cells"""
    # Constant default values
    THERMAL_CAPACITY = 1243
    THERMAL_CONDUCTIVITY_AXIAL = 21
    THERMAL_CONDUCTIVITY_RADIAL = 0.48
    def __init__(
        self, freighttype, dimensions, weight, 
        thermalcapacity = THERMAL_CAPACITY, 
        thermalconductivity = [
            THERMAL_CONDUCTIVITY_RADIAL,
            THERMAL_CONDUCTIVITY_RADIAL,
            THERMAL_CONDUCTIVITY_AXIAL
        ]
        ):
        if freighttype not in FREIGHTTYPES:
            raise ValueError("Freight: freighttype must be one of %r." % FREIGHTTYPES)
        self.type = freighttype
        self.dimensions = dimensions
        self.weight = weight
        self.thermalcapacity = thermalcapacity
        self.thermalconductivity = thermalconductivity

    def density(self):
        volume = np.prod(self.dimensions)
        if volume == 0:
            raise ValueError('Volume of freight is 0. Check dimensions of freight.')
        return self.weight / volume

    def location_elements(self, dimensions_package):
        """Get array of center points of each freightelement in one package in the initial coordinate system (0, 0, 0)"""
        elements_in_package = self.elements_in_package(dimensions_package)
        points_x = np.linspace(-dimensions_package[0]/2, dimensions_package[0]/2, elements_in_package[0] * 3 + 2)[2::3]
        points_y = np.linspace(-dimensions_package[1]/2, dimensions_package[1]/2, elements_in_package[1] * 3 + 2)[2::3] 
        points_z = np.linspace(-dimensions_package[2]/2, dimensions_package[2]/2, elements_in_package[2] * 3 + 2)[2::3]
        return np.vstack(np.meshgrid(points_x, points_y, points_z)).reshape(3,-1).T

    def elements_in_package(self, dimensions_package):
        """Returns list with number of individual freight elements per axis"""
        result = [floor(dimensions_package[i] / self.dimensions[i]) for i in range(len(self.dimensions))]
        if np.prod(result) == 0:
            raise ValueError('Freight does not fit into packaging. Check dimensions of freight against dimensions of package.')
        else:
            return result

    def to_dict(self):
        return {
            'type': self.type,
            'dimensions': self.dimensions,
            'weight': self.weight,
            'thermalcapacity': self.thermalcapacity,
            'thermalconductivity': self.thermalconductivity
        }

def freightDecoder(obj):
    return Freight(
        obj['type'], obj['dimensions'], float(obj['weight']), 
        thermalcapacity = obj.get('thermalcapacity', Freight.THERMAL_CAPACITY),
        thermalconductivity = obj.get(
            'thermalconductivity', [
                Freight.THERMAL_CONDUCTIVITY_RADIAL,
                Freight.THERMAL_CONDUCTIVITY_RADIAL,
                Freight.THERMAL_CONDUCTIVITY_AXIAL
            ]
            )       
        )

