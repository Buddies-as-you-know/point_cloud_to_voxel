import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# 以前のスクリプトからのデータを読み込む
pcd_xz = o3d.io.read_point_cloud("output_xz.ply")
pcd_yz = o3d.io.read_point_cloud("output_yz.ply")

# 点群をnumpy配列に変換
points_xz = np.asarray(pcd_xz.points)
points_yz = np.asarray(pcd_yz.points)

# Z座標でグループ化
z_coords = set(points_xz[:, 2]) & set(points_yz[:, 2])

# 各Z座標でループ
final_points = []
for z in z_coords:
    # 各Z平面での点を取得
    points_in_z_xz = points_xz[points_xz[:, 2] == z]
    points_in_z_yz = points_yz[points_yz[:, 2] == z]

    # XとY座標を取得
    x_coords = set(points_in_z_xz[:, 0])
    y_coords = set(points_in_z_yz[:, 1])

    # Cartesian productを計算
    cartesian_product = [(x, y, z) for x in x_coords for y in y_coords]
    final_points.extend(cartesian_product)

# 最終的な点群をOpen3DのPoint Cloudオブジェクトに変換
final_pcd = o3d.geometry.PointCloud()
final_pcd.points = o3d.utility.Vector3dVector(np.array(final_points))

# 結果を表示
# o3d.visualization.draw_geometries([final_pcd])

# 結果を保存
o3d.io.write_point_cloud("output_final.ply", final_pcd)
