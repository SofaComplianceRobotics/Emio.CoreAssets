# Use this script to resample your beam meshes (.txt file used in the Emio Labs application) 
# by interpolating positions and slerping rotations. This can be useful to reduce the number 
# of points in the mesh for faster simulations, or to increase it for better accuracy. 
# You can run this script from the command line as follows:
# python beam_resampler.py input_mesh.txt output_mesh.txt num_points

import numpy as np
import argparse
import os

def plotMeshes(originalFile, resampledFile):
    """Plot the original and resampled meshes side by side for comparison."""
    import matplotlib.pyplot as plt

    originalFrames = np.loadtxt(originalFile)
    print(originalFrames[:, :3])
    resampledFrames = np.loadtxt(resampledFile)

    fig = plt.figure(figsize=(12, 6))

    # The mesh is in mm 
    # We fix the scale of the plot to be the same for both meshes, and to be in mm, so that we can compare them easily
    # We also fix the scale of each axis to be the same, so that the shape of the meshes is not distorted
    allFrames = np.vstack([originalFrames, resampledFrames])
    min_vals = np.min(allFrames[:, :3], axis=0)
    max_vals = np.max(allFrames[:, :3], axis=0)
    margin = 10  # Add a margin of 10 mm around the meshes
    min_vals -= margin
    max_vals += margin
    min_val = min(min_vals)
    max_val = max(max_vals)

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_xlim(min_val, max_val)
    ax1.set_ylim(min_val, max_val)
    ax1.set_zlim(min_val, max_val)
    ax1.set_title('Original Mesh')
    ax1.plot(originalFrames[:, 0], originalFrames[:, 1], originalFrames[:, 2], 'o-')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_xlim(min_val, max_val)
    ax2.set_ylim(min_val, max_val)
    ax2.set_zlim(min_val, max_val)
    ax2.set_title('Resampled Mesh')
    ax2.plot(resampledFrames[:, 0], resampledFrames[:, 1], resampledFrames[:, 2], 'o-')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    plt.show()

def checkFileExists(file: str) -> str:
    """Check if the file exists at the given path, or in the current directory 
    or in ~/emio-labs/version/assets/data/meshes/legs/ and return the path to the file.
    """
    # First check if the file exists at the given path
    if not os.path.exists(file):
        # Check if the file is located in the current directory
        if not os.path.exists(os.path.join(os.getcwd(), file)):
            # Check if the file is located in the current directory /data/meshes/legs/
            if not os.path.exists(os.path.join(os.getcwd(), 'data', 'meshes', 'legs', file)):
                raise FileNotFoundError(f"The file {file} was not found at the given path, nor in the current directory, nor in the current directory/data/meshes/legs/")
            else:
                return os.path.join(os.getcwd(), 'data', 'meshes', 'legs', file)
        else:
            return os.path.join(os.getcwd(), file)
    else:
        return file

def resampleBeamMesh(filename, newFilename, nbPoints):
    """Resample a beam mesh by interpolating positions and slerping rotations."""

    for file in [filename, newFilename]:
        if not file.endswith('.txt'):
            raise ValueError(f"The file {file} must have a .txt extension.")
    
    filename = checkFileExists(filename)
    if not os.path.exists(os.path.dirname(newFilename)):
        # If the directory of the output file does not exist, we use the same directory as the input file
        newFilename = os.path.join(os.path.dirname(filename), os.path.basename(newFilename))
        print(f"The directory of the output file does not exist. The resampled mesh will be saved as {newFilename} instead.")

    # If the output file already exists, we ask the user if they want to overwrite it
    if os.path.exists(newFilename):
        overwrite = input(f"The file {newFilename} already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled. Please provide a different output file name.")
            exit()

    frames = np.loadtxt(filename)

    # Each frame is represented by 7 values (3 for position and 4 for orientation as a quaternion)
    # The quaternion follows SOFA convention (qx, qy, qz, qw)
    # The direction of the beam is given by the x-axis of the local frame, which can be computed from the quaternion.
    if frames.shape[1] != 7:
        raise ValueError("The input file must contain frames with 7 values (3 pos, 4 quat).")
    
    # The two first frames correspond to the part of the leg that is fixed to the motor, 
    # we keep them as they are and resample only the rest of the frames
    fixedFrames = frames[:1]
    frames = frames[1:]

    n = len(frames)
    if nbPoints <= 0:
        raise ValueError("nbPoints must be > 0")

    original_idx = np.arange(n)
    desired_idx = np.linspace(0, n - 1, nbPoints)

    # positions: cubic if enough points, else linear
    from scipy.interpolate import interp1d
    kind = 'cubic' if n >= 4 else 'linear'
    pos_interp = interp1d(original_idx, frames[:, :3], axis=0, kind=kind)
    resampled_pos = pos_interp(desired_idx)

    # rotations: use Slerp on quaternions (expects [x, y, z, w])
    from scipy.spatial.transform import Rotation, Slerp
    rots = Rotation.from_quat(frames[:, 3:7])
    slerp = Slerp(original_idx, rots)
    resampled_rots = slerp(desired_idx)
    resampled_quats = resampled_rots.as_quat()

    resampledFrames = np.hstack([resampled_pos, resampled_quats])
    # We add the fixed frames at the beginning of the resampled frames
    resampledFrames = np.vstack([fixedFrames, resampledFrames])
    np.savetxt(newFilename, resampledFrames)
    plotMeshes(filename, newFilename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resample a beam mesh (.txt file used in the Emio Labs application).')
    parser.add_argument('input_file', type=str, help='Path to the input .txt file containing the original mesh.')
    parser.add_argument('output_file', type=str, help='Path to the output .txt file where the resampled mesh will be saved.')
    parser.add_argument('num_points', type=int, help='The desired number of points in the resampled mesh.')

    args = parser.parse_args()

    resampleBeamMesh(args.input_file, args.output_file, args.num_points)