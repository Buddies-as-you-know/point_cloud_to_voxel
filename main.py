from src.histogram_point_generator import process_point_cloud
import os
if __name__ == "__main__":
    bin_size = 1.0
    threshold = 1000  # Adjust this value based on your requirement
    pwd = os.getcwd()
    process_point_cloud(pwd + "/data/_point_cloud.ply", threshold, bin_size)