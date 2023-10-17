import open3d as o3d
import numpy as np
import os
import numpy as np
from plyfile import PlyData
from collections import defaultdict
import csv
import math
from collections import defaultdict

# .plyファイルからデータを読み込む関数
def read_ply_file(filepath):
    vertices = []

    # PlyDataを使用してファイルを読み込む
    plydata = PlyData.read(filepath)

    # 'vertex'要素にアクセスし、頂点データを取得
    for vertex in plydata['vertex']:
        x, z = vertex['x'], vertex['z']  # y座標は無視
        vertices.append((x, z))

    return vertices
# XZ座標に基づいて頂点を集計する関数
def create_histogram(vertices, bin_size):
    """
    与えられたbin_sizeに基づいて、点のXZ座標を丸め、ヒストグラムを作成します。
    """
    histogram = defaultdict(int)

    for x, z in vertices:
        # 座標をbin_sizeに「丸める」
        binned_x = math.floor(x / bin_size) * bin_size
        binned_z = math.floor(z / bin_size) * bin_size

        # 丸められた座標をキーとして使用し、そのバケットの点の数を増やす
        histogram[(binned_x, binned_z)] += 1

    return histogram


# 結果をCSVファイルに書き込む関数
def write_to_csv(counter, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['X', 'Z', 'Count'])  # CSVのヘッダ行
        for (x, z), count in counter.items():
            writer.writerow([x, z, count])  # 各行にX, Z座標と一致する点の数を書き込む


# メイン処理

def main(ply_file_path, csv_output_path, bin_size):
    vertices = read_ply_file(ply_file_path)
    histogram = create_histogram(vertices, bin_size)
    write_to_csv(histogram, csv_output_path)

# bin_sizeは、点をグループ化する際の「バケット」のサイズを決定します。
# この値を変更することで、ヒストグラムの粒度を調整できます。
bin_size = 1.0  # 例として1.0を使用
pwd = os.getcwd()
print(main(pwd+"/data/_point_cloud.ply","./xz_count.csv",bin_size))