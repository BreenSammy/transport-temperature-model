# Dictionaries for OpenFOAM boundary conditions

region_coupling_fluid = {
    'type': 'compressible::turbulentTemperatureCoupledBaffleMixed',        
    'Tnbr': 'T',
    'thicknessLayers': '( 1 )',
    'kappaLayers': '( 1 )',
    'kappaMethod': 'fluidThermo',
    'value': '$internalField'
}

region_coupling_solid_anisotrop = {
    'type': 'compressible::turbulentTemperatureCoupledBaffleMixed',        
    'Tnbr': 'T',
    'thicknessLayers': '( 1 )',
    'kappaLayers': '( 1 )',
    'kappaMethod': 'directionalSolidThermo',
    'alphaAni': 'Anialpha',
    'value': '$internalField'
}