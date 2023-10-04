import open3d as o3d
import numpy as np
from scipy.spatial import Delaunay

# 点群データをロード
pcd = o3d.io.read_point_cloud("output_union.ply")
points = np.asarray(pcd.points)

# Z座標を無視してXY座標だけを取得
xy_coords = points[:, :2]

# Delaunay 三角化
triangles = Delaunay(xy_coords)

# Open3DのTriangleMeshオブジェクトを作成
mesh = o3d.geometry.TriangleMesh()

# 頂点を追加
mesh.vertices = o3d.utility.Vector3dVector(points)

# 三角形を追加
mesh.triangles = o3d.utility.Vector3iVector(triangles.simplices)

# メッシュを表示 (オプショナル)
# o3d.visualization.draw_geometries([mesh])

# メッシュを保存
o3d.io.write_triangle_mesh("output_mesh.ply", mesh)