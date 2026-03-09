:::::: collapse Beam Resampler

# Beam Resampler

This section allows you to resample a beam mesh of a leg (in `.txt` format used in the Emio Labs application) 
by interpolating positions and slerping rotations. 
This can be useful to reduce the number of points in the mesh for faster simulations, or to increase it for better accuracy.

The `.txt` file should contain frames of the beam mesh, where each frame is represented by 7 values:
- 3 values for the position (x, y, z)
- 4 values for the orientation as a quaternion (qx, qy, qz, qw) following the SOFA convention. The direction of the beam is given by the x-axis of the local frame, which can be computed from the quaternion.
- The two first frames correspond to the part of the leg that is fixed to the motor, we keep then as it is and resample only the rest of the frames.

You need to provide the path to the `input` .txt file containing the original mesh, the path to the `output` .txt file 
where the resampled mesh will be saved. Either provide an absolute path, or a relative path from the current working directory, or only the filename if it is in the current working directory `/data/meshes/legs/`. Also provide the desired `number of points` in the resampled mesh. Then click the python button to run the resampling script.

::::: group-grid {style="grid-template-rows:repeat(2, 0fr)"}
**Input Filename**
#input("InputLegFilename", "path to the input .txt file containing the original mesh")

**Output Filename**
#input("OutputLegFilename", "path to the output .txt file where the resampled mesh will be saved")
:::::

::::: group-grid {style="grid-template-rows:repeat(2, 0fr)"}
**Number of Points**
#input("NumPoints", "the desired number of points in the resampled mesh")
:::::

#python-button("'assets/labs/modules/beam_resampler.py' InputLegFilename OutputLegFilename NumPoints")

::::::