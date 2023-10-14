import open3d as o3d
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
import plyfile

import numpy as np
from plyfile import PlyData
from collections import defaultdict
import csv

def count_points_per_y_level(ply_file_path, csv_output_path):
    # Load the .ply file
    plydata = PlyData.read(ply_file_path)
    
    # Extract vertex data
    vertex_data = plydata['vertex'].data
    
    # Extract x, y, z coordinates
    x = vertex_data['x']
    y = vertex_data['y']
    z = vertex_data['z']
    
    # Combine x, y, z into a 2D numpy array
    points = np.vstack((x, y, z)).T
    
    # Create a dictionary to store the count of points at each y level
    points_count_at_y = defaultdict(int)
    
    # Loop through all points and count the occurrences at each y level
    for point in points:
        y_level = point[1]  # extract the y coordinate
        points_count_at_y[y_level] += 1  # increment the counter for this y level
    
    # Write the results to a .csv file
    with open(csv_output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Y_Level", "Point_Count"])  # Write header
        for y_level, count in points_count_at_y.items():
            writer.writerow([y_level, count])  # Write data rows

# Example usage:
# count_points_per_y_level('path_to_your_ply_file.ply', 'output.csv')

# Example usage:
# ply_file_path = 'path_to_your_file.ply'
# y_value = 10.0
# num_points_on_plane = count_points_on_plane(ply_file_path, y_value)
# print(f'Number of points on the plane: {num_points_on_plane}')

# ステップ1: .ply ファイルをロード
pwd = os.getcwd()
count_points_per_y_level(pwd+"/data/_point_cloud.ply","./xz_count.csv")