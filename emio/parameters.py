# Parameters of the soft parts (TPU filament: https://shop3d.ca/collections/flexible-filaments-tpu/products/bambu-lab-tpu-hf-1-75mm-1kg)
youngModulus = 3.5e4 # This has been measured for the beam models. In the labs, a factor of 'tetraYMFactor'
# is applied when using the tetra model (because of the artificial rigidity introduced by the mesh discretization).
tetraYMFactor = 0.2
poissonRatio = 0.45
massDensity = 1.220e-6
# Parameters of the legs, for beam and cosserat models
width = 10
thickness = 5
# Camera parameters
cameraTranslation = [147, 5]  # [xz, y] in mm