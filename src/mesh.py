import numpy as np
import open3d as o3d
from scipy.spatial import ConvexHull
from skimage import measure
import os
def voxelization(points, voxel_size=0.05):
    """
    ボクセル化関数
    :param points: 点群データ (numpy array)
    :param voxel_size: ボクセルのサイズ
    :return: ボクセルグリッド、ボクセルの占有情報
    """
    # 点群データをOpen3Dの形式に変換
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    # ボクセルグリッドのダウンサンプリング
    voxels = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)

    # ボクセルの中心を取得
    voxel_centers = np.asarray(voxels.get_voxels())[:, :3]

    return voxels, voxel_centers

def marching_cubes(voxel_centers, occupancy, shape, level=0.5):
    """
    マーチングキューブアルゴリズム関数
    :param voxel_centers: ボクセルの中心のリスト
    :param occupancy: 各ボクセルの占有率
    :param shape: グリッドの形状
    :param level: サーフェスを抽出するためのしきい値
    :return: メッシュの頂点と面
    """
    # ボクセルグリッド内の占有率を3D配列に整理
    occupancy_grid = np.zeros(shape)
    for center, occ in zip(voxel_centers, occupancy):
        x, y, z = center
        occupancy_grid[int(x), int(y), int(z)] = occ

    # マーチングキューブアルゴリズムの適用
    verts, faces, normals, values = measure.marching_cubes_lewiner(occupancy_grid, level)

    return verts, faces

def main(ply_file, voxel_size=0.05):
    """
    メイン関数
    :param ply_file: .plyファイルのパス
    :param voxel_size: ボクセルのサイズ
    """
    # 点群データの読み込み
    pcd = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(pcd.points)

    # 占有率のボクセル化
    voxels, voxel_centers = voxelization(points, voxel_size)

    # ここで、占有率の計算を行います。この例では、すべてのボクセルを占有していると仮定します。
    # 実際のアプリケーションでは、センサーデータや他の情報に基づいて、各ボクセルの占有率を計算する必要があります。
    occupancy = np.ones(len(voxel_centers))

    # グリッドの形状を計算（ボクセルの最大値に基づく）
    shape = tuple(np.max(voxel_centers, axis=0).astype(int) + 1)

    # マーチングキューブアルゴリズムの適用
    verts, faces = marching_cubes(voxel_centers, occupancy, shape)

    # メッシュの生成と表示
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(verts)
    mesh.triangles = o3d.utility.Vector3iVector(faces)
    o3d.visualization.draw_geometries([mesh])

if __name__ == "__main__":
    # .plyファイルのパスを指定します。
    pwd = os.getcwd()
    ply_file_path = pwd + "/point_cloud_data/_point_cloud.ply"
    main(ply_file_path)
