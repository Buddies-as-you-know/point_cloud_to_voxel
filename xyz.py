import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from collections import defaultdict

# それぞれの平面に射影されたデータをロード
xz_pcd = o3d.io.read_point_cloud("output_xz.ply")
yz_pcd = o3d.io.read_point_cloud("output_yz.ply")

# ポイントとカラーをnumpy配列に変換
xz_points = np.asarray(xz_pcd.points)
yz_points = np.asarray(yz_pcd.points)
xz_colors = np.asarray(xz_pcd.colors)
yz_colors = np.asarray(yz_pcd.colors)

# Z軸の値をキーとするディクショナリを作成し、対応するXおよびY座標のリストを保持
xz_dict = defaultdict(list)
yz_dict = defaultdict(list)

for point, color in zip(xz_points, xz_colors):
    xz_dict[point[2]].append((point[0], color))

for point, color in zip(yz_points, yz_colors):
    yz_dict[point[2]].append((point[1], color))

# 新しい点群とカラーのリストを作成
new_points = []
new_colors = []

# Z軸の値ごとにループを回し、XおよびY座標を統合
for z in set(xz_dict.keys()) & set(yz_dict.keys()):
    xz_entries = xz_dict[z]
    yz_entries = yz_dict[z]

    for xz_entry, yz_entry in zip(xz_entries, yz_entries):
        x, x_color = xz_entry
        y, y_color = yz_entry
        new_points.append([x, y, z])
        # ここでは平均カラーを使用していますが、他の方法も使用可能です。
        new_colors.append(((np.array(x_color) + np.array(y_color)) / 2).tolist())

# 新しい点群をOpen3DのPoint Cloudオブジェクトに変換
new_pcd = o3d.geometry.PointCloud()
new_pcd.points = o3d.utility.Vector3dVector(np.array(new_points))
new_pcd.colors = o3d.utility.Vector3dVector(np.array(new_colors))

# 結果を表示（オプション）
#o3d.visualization.draw_geometries([new_pcd])

# 結果を保存
o3d.io.write_point_cloud("output_xyz.ply", new_pcd)
