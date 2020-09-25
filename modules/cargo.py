import os

import numpy as np
from PyFoam.Basics.DataStructures import Vector

NUMBER_PACKAGES = {
    'pallet1x4.stl': 4,
    'pallet2x4.stl': 8,
    'pallet3x4.stl': 12,
    'industrial_pallet1x1.stl': 1,
    'industrial_pallet1x4.stl': 4
}

class Battery:
    def __init__(self, position):
        self.position = position
        self.name = None
        self.temperature = None

class Pallet:
    """Class to describe a pallet full of packages filled with batteries."""
    def __init__(self, templateSTL: str, position: list, orientation: list):
        self.type = 'Pallet'
        self.templateSTL = templateSTL
        self.position = position
        self.orientation = orientation
        self.batteries = []

        # Save positions of seperate packages for locationsInMesh in snappyHexMeshDict 
        position_vector = Vector(position[0], position[1], position[2])
        number_packages = NUMBER_PACKAGES[self.templateSTL]
        
        for i in range(int(number_packages/4)):
            z_coordinate = self.position[2] + 0.15505 + 0.400*i
            self.batteries.extend([
                Battery(position_vector.__add__(Vector(0.201, 0.201, z_coordinate))), 
                Battery(position_vector.__add__(Vector(0.201, -0.201, z_coordinate))),
                Battery(position_vector.__add__(Vector(-0.201, -0.201, z_coordinate))), 
                Battery(position_vector.__add__(Vector(-0.201, 0.201, z_coordinate))),
            ])

    def vector_to_string(self, vector):
        """Transform a vector with three entries into a string for terminal commands"""
        return "'(" + str(vector[0]) + ' ' + str(vector[1]) + ' ' + str(vector[2]) + ")'"
    
    def move_STL(self, case, target):
        """Move the STL to the right position in the carrier."""

        # Copy STL form template STL and bring it in the right orientation
        os.system(
            'surfaceTransformPoints -rollPitchYaw ' + self.vector_to_string(self.orientation) + " " + 
            os.path.join(case.constantDir(), "triSurface", self.templateSTL) + " " + 
            os.path.join(case.constantDir(), "triSurface", target)
            )

        # Move STL to its position
        os.system(
            'surfaceTransformPoints -translate ' + self.vector_to_string(self.position) + " " + 
            os.path.join(case.constantDir(), "triSurface", target) + " " + 
            os.path.join(case.constantDir(), "triSurface", target)
            )
        self.STL = target

    def to_dict(self):
        """Transform essential attributes of pallet to dict to save as json in Transport class"""
        return {
            'Type': 'Pallet',
            'TemplateSTL': self.templateSTL,
            'Position': self.position,
            'Orientation': self.orientation 
        }

def cargoDecoder(obj):
    if obj['Type'] == 'Pallet':
        return Pallet(obj['TemplateSTL'], obj['Position'], obj['Orientation'])