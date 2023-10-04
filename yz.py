import open3d as o3d
import numpy as np
import os
import matplotlib.pyplot as plt
# ステップ1: .ply ファイルをロード
pwd = os.getcwd()
pcd = o3d.io.read_point_cloud(pwd+"/data/_point_cloud.ply")


# ステップ2: X軸を潰してYZ平面に投影
point_cloud_data = np.asarray(pcd.points)
projected_points = point_cloud_data[:, 1:]

# ステップ2: 2Dヒストグラム作成
hist, xedges, yedges = np.histogram2d(projected_points[:,0], projected_points[:,1], bins=(100, 100))

# ステップ3: 閾値を設定して地面を識別
threshold = 10  # 適切な値を選ぶ必要があります
ground_mask = hist > threshold

# ステップ4: 可視化
plt.imshow(ground_mask, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
plt.title('Identified Ground Region in YZ Plane')
plt.xlabel('Y')
plt.ylabel('Z')
plt.show()