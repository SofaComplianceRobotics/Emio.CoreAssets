# data/meshes/centerparts

Add your custom mesh files here. 

For the connector / centerpart, you should provide:

1. A surface mesh in the `.stl` format for the visualization.
2. A `.json` file defining the positions and orientations for attaching the legs.
3. [Optional] A volume mesh in the `.vtk` format, if you want to use the tetra model (deformable option).

The name of the file should match, for example:

1. `bluepart.stl`
2. `bluepart.vtk`
3. `bluepart.json`

Here is an example of a `.json` file, in `emio-labs/assets/data/meshes/centerparts/bluepart.json`:

```json
{
  "initialPosition":
  [
    [0, -150, 0, 1, 0, 0, 0]
  ],
  "attachPositionInLocalCoord":
 [
   [  0, -3,-10,  0.500, -0.500,  0.500,  0.500],
   [ 10, -3,  0,  0.000,  0.707,  0.707,  0.000],
   [  0, -3, 10, -0.500, -0.500,  0.500, -0.500],
   [-10, -3,  0, -0.707, -0.000, -0.000,  0.707]
 ]
}
```

- `initialPosition`: corresponds to the initial position of the part in the simulation. You should keep it the same. 
- `attachPositionInLocalCoord`: for each leg, the position and orientation of attachements relative to the mesh origin [x, y, z, qx, qy, qz, qw] 

