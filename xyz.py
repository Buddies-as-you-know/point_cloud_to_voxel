import open3d as o3d
import numpy as np

# 既存の点群をロード
pcd_xz = o3d.io.read_point_cloud("output_xz.ply")
pcd_yz = o3d.io.read_point_cloud("output_yz.ply")

# 2つの点群を結合
combined_pcd = pcd_xz + pcd_yz

# 結果を表示 (オプショナル)
# o3d.visualization.draw_geometries([combined_pcd])

# 結果を保存
o3d.io.write_point_cloud("output_union.ply", combined_pcd)
