import open3d as o3d
import numpy as np
import os

import open3d as o3d
import numpy as np

if __name__ == "__main__":
    # PLYファイルから点群を読み込む
    pwd = os.getcwd()
    ptCloud = o3d.io.read_point_cloud(pwd+"/data/_point_cloud.ply")

# Normal estimation
    ptCloud.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    print(1)
    # Orientation of normal vector is consistent with tangent plane 
    ptCloud.orient_normals_consistent_tangent_plane(10)
    print(2)   
    # Surface reconstruction by ball pivoting algorithm
    distances = ptCloud.compute_nearest_neighbor_distance()
    print(3)
    avg_dist = np.mean(distances)
    radius = 2*avg_dist   
    radii = [radius, radius * 2]
    recMeshBPA = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
            ptCloud, o3d.utility.DoubleVector(radii))
    print(4)  
     # Visualization in window (BPA)
    o3d.visualization.draw_geometries([recMeshBPA])