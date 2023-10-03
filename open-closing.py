import open3d as o3d
import numpy as np
from scipy.ndimage import binary_opening, binary_closing, generate_binary_structure
import os
def process_3d_data(data):
    selem_opening_small = generate_binary_structure(3, 1)  # 3x3x3
    selem_closing_large = generate_binary_structure(3, 2)  # 9x9x5
    
    data_opened = binary_opening(data, structure=selem_opening_small)
    data_closed = binary_closing(data_opened, structure=selem_closing_large)
    data_opened_large = binary_opening(data_closed, structure=selem_closing_large)
    
    return data_opened_large
pwd = os.getcwd()
pcd = o3d.io.read_point_cloud(pwd+"/data/_point_cloud.ply")
# Convert point cloud to voxel grid
# Convert point cloud to voxel grid
voxel_size = 0.05
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)

# Get the occupied voxels
occupied_voxels = np.asarray([voxel.grid_index for voxel in voxel_grid.get_voxels()])

# Create a dense voxel grid using a 3D numpy array
max_bound = np.max(occupied_voxels, axis=0) + 1
voxel_np = np.zeros(max_bound, dtype=np.uint8)
for v in occupied_voxels:
    voxel_np[tuple(v)] = 1

# Process the voxel data
processed_data = process_3d_data(voxel_np)

# Convert processed voxel data to point cloud for visualization
x, y, z = np.where(processed_data > 0)
points = np.vstack((x, y, z)).T * voxel_size  # Apply voxel size scaling
pcd_processed = o3d.geometry.PointCloud()
pcd_processed.points = o3d.utility.Vector3dVector(points)

# Visualize the original and processed point clouds
o3d.visualization.draw_geometries([pcd, pcd_processed])