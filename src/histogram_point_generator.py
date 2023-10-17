import open3d as o3d
import numpy as np
import os
from plyfile import PlyData
from collections import defaultdict
import math

def read_ply_file(filepath):
    vertices = []
    plydata = PlyData.read(filepath)
    for vertex in plydata['vertex']:
        x, y, z = vertex['x'], vertex['y'], vertex['z']
        vertices.append((x, y, z))
    return vertices

def create_histogram(vertices, bin_size):
    histogram_xz = defaultdict(int)
    histogram_yz = defaultdict(int)
    for x, y, z in vertices:
        binned_x = math.floor(x / bin_size)
        binned_y = math.floor(y / bin_size)
        binned_z = math.floor(z / bin_size)
        histogram_xz[(binned_x, binned_z)] += 1
        histogram_yz[(binned_y, binned_z)] += 1
    return histogram_xz, histogram_yz

def threshold_histogram(histogram, threshold):
    return {k: v for k, v in histogram.items() if v > threshold}

def generate_points(histogram_xz, histogram_yz):
    new_vertices = []

    for (x, z), count in histogram_xz.items():
        for _ in range(count):
            new_vertices.append((x, 0, z))  # y-coordinate is set to 0

    for (y, z), count in histogram_yz.items():
        for _ in range(count):
            new_vertices.append((0, y, z))  # x-coordinate is set to 0

    return new_vertices

def process_point_cloud(ply_file_path, threshold, bin_size):
    vertices = read_ply_file(ply_file_path)
    histogram_xz, histogram_yz = create_histogram(vertices, bin_size)
    thresholded_histogram_xz = threshold_histogram(histogram_xz, threshold)
    thresholded_histogram_yz = threshold_histogram(histogram_yz, threshold)
    new_vertices = generate_points(thresholded_histogram_xz, thresholded_histogram_yz)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(new_vertices)
    pwd = os.getcwd()
    o3d.io.write_point_cloud(pwd + "/point_cloud_data/new_point_cloud.ply", pcd)

if __name__ == "__main__":
    bin_size = 0.5
    threshold = 1000  # Adjust this value based on your requirement
    pwd = os.getcwd()
    process_point_cloud(pwd + "/point_cloud_data/_point_cloud.ply", threshold, bin_size)
