import os

import numpy as np

from PyFoam.Basics.DataStructures import Vector

class Pallet:
    """Class to describe a pallet full of packages."""
    def __init__(self, name: str, STL: str, number_packages: int, position: np.array, orientation: np.array):
        self.name = name
        self.STL = STL
        self.number_packages = number_packages
        self.position = position
        self.orientation = orientation
        position_vector = Vector(position[0], position[1], position[2])
        
        # Save positions of seperate packages for locationsInMesh in snappyHexMeshDict
        self.package_positions = []
        for i in range(int(self.number_packages/4)):
            z_coordinate = self.position[2] + 0.15505 + 0.400*i
            self.package_positions.extend([
                position_vector.__add__(Vector(0.201, 0.201, z_coordinate)), position_vector.__add__(Vector(0.201, -0.201, z_coordinate)),
                position_vector.__add__(Vector(-0.201, -0.201, z_coordinate)), position_vector.__add__(Vector(-0.201, 0.201, z_coordinate)),
            ])

    def vector_to_string(self, vector):
        """Transform a vector with three entries into a string for terminal commands"""
        return "'(" + str(vector[0]) + ' ' + str(vector[1]) + ' ' + str(vector[2]) + ")'"
    
    def move_STL(self, case, target):
        """Move the STL to the right position in the carrier."""

        # Copy STL form template STL and bring it in the right orientation
        os.system(
            'surfaceTransformPoints -rollPitchYaw ' + self.vector_to_string(self.orientation) + " " + 
            os.path.join(case.constantDir(), "triSurface", self.STL) + " " + 
            os.path.join(case.constantDir(), "triSurface", target)
            )

        # Move STL to its position
        os.system(
            'surfaceTransformPoints -translate ' + self.vector_to_string(self.position) + " " + 
            os.path.join(case.constantDir(), "triSurface", target) + " " + 
            os.path.join(case.constantDir(), "triSurface", target)
            )
        self.STL = target