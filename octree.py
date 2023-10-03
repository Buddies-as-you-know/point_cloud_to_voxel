import open3d as o3d
import numpy as np
import os
from scipy import ndimage
from scipy.ndimage import binary_opening, binary_closing, label
if __name__ == "__main__":

    # Loading point cloud
    print("Loading point cloud")
    pwd = os.getcwd()
    pcd = o3d.io.read_point_cloud(pwd+"/data/_point_cloud.ply")

    # Octreeのパラメータを設定
    max_depth = 8  # Octreeの最大深さ

    # Octreeを構築
    octree = o3d.geometry.Octree(max_depth=max_depth)
    octree.convert_from_point_cloud(pcd)

    # 可視化
    o3d.visualization.draw_geometries([octree])