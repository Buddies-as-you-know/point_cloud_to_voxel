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

    # 点群をNumPy配列に変換
    points = np.asarray(pcd.points)

    # 座標の最小値と最大値を取得して、ボクセルグリッドを作成
    min_coords = points.min(axis=0)
    max_coords = points.max(axis=0)
    voxel_size = 0.05
    grid_shape = np.ceil((max_coords - min_coords) / voxel_size).astype(int)
    binary_array = np.zeros(grid_shape, dtype=bool)

    # 点群の座標をボクセルグリッドのインデックスに変換
    indices = ((points - min_coords) / voxel_size).astype(int)
    binary_array[indices[:, 0], indices[:, 1], indices[:, 2]] = 1

    # 3Dオープニング処理
    struct_element = np.ones((3, 3, 3))
    opened_array = binary_opening(binary_array, structure=struct_element)

    # 3Dクロージング処理
    closed_array = binary_closing(opened_array, structure=struct_element)

    # 処理されたボクセルグリッドからの座標を取得
    closed_coords = np.argwhere(closed_array)
    closed_coords = closed_coords * voxel_size + min_coords

    # 処理された座標を点群に変換
    processed_pcd = o3d.geometry.PointCloud()
    processed_pcd.points = o3d.utility.Vector3dVector(closed_coords)

    # 処理された点群を保存
    o3d.io.write_point_cloud("output.ply", processed_pcd)
    pcd = o3d.io.read_point_cloud("output.ply")
    o3d.visualization.draw_geometries([pcd])
