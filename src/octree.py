import open3d as o3d
import numpy as np
import os
from scipy import ndimage
from scipy.ndimage import binary_opening, binary_closing, label
from scipy.spatial import Delaunay
def interpolate_missing_points(ply_file):
    # PLYファイルから点群を読み込む
    pcd = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(pcd.points)

    # Delaunay Triangulationを使用して三角形を作成
    tri = Delaunay(points[:,:2])

    # 欠損している点を三角形の頂点の平均値で補完
    for simplex in tri.simplices:
        # 三角形の3つの頂点を取得
        vertices = points[simplex]
        
        # 頂点の平均値を計算
        avg_vertex = np.mean(vertices, axis=0)
        
        # 平均値を点群に追加
        points = np.vstack([points, avg_vertex])
    
    # 更新された点群をPCDオブジェクトに変換
    pcd.points = o3d.utility.Vector3dVector(points)
    pwd = os.getcwd()
    # 補完された点群を保存
    o3d.io.write_point_cloud(pwd + "/data/interpolated.ply", pcd)
if __name__ == "__main__":

    # Loading point cloud
    print("Loading point cloud")
    pwd = os.getcwd()
    ply_file = pwd+"/data/_full_mesh.ply"
    interpolate_missing_points(ply_file)
    pcd = o3d.io.read_point_cloud(pwd+"/data/_point_cloud.ply")

    # Octreeのパラメータを設定
    max_depth = 8  # Octreeの最大深さ

    # Octreeを構築
    octree = o3d.geometry.Octree(max_depth=max_depth)
    octree.convert_from_point_cloud(pcd)

    # 可視化
    o3d.visualization.draw_geometries([octree])