import open3d as o3d
import numpy as np
import os
import numpy as np
from plyfile import PlyData
from collections import defaultdict
import csv
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
        binned_x = math.floor(x / bin_size) * bin_size
        binned_y = math.floor(y / bin_size) * bin_size
        binned_z = math.floor(z / bin_size) * bin_size

        histogram_xz[(binned_x, binned_z)] += 1
        histogram_yz[(binned_y, binned_z)] += 1

    return histogram_xz, histogram_yz

def threshold_histogram(histogram, threshold):
    return {k: v for k, v in histogram.items() if v > threshold}

def generate_points(histogram_xz, histogram_yz):
    new_vertices = []

    common_z_values = set(z for x, z in histogram_xz.keys()) & set(z for y, z in histogram_yz.keys())

    for z in common_z_values:
        for x, _ in ((x, z) for x, z in histogram_xz.keys() if z == z):
            for y, _ in ((y, z) for y, z in histogram_yz.keys() if z == z):
                new_vertices.append((x, y, z))

    return new_vertices

def main(ply_file_path, threshold, bin_size):
    vertices = read_ply_file(ply_file_path)
    histogram_xz, histogram_yz = create_histogram(vertices, bin_size)
    thresholded_histogram_xz = threshold_histogram(histogram_xz, threshold)
    thresholded_histogram_yz = threshold_histogram(histogram_yz, threshold)
    new_vertices = generate_points(thresholded_histogram_xz, thresholded_histogram_yz)

    # Create and save new point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(new_vertices)
    o3d.io.write_point_cloud("new_point_cloud.ply", pcd)

bin_size = 1.0
threshold = 1000  # Adjust this value based on your requirement
pwd = os.getcwd()
main(pwd + "/data/_point_cloud.ply", threshold, bin_size)
