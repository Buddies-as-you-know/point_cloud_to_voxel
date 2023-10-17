from src.histogram_point_generator import process_point_cloud
import os
if __name__ == "__main__":
    bin_size = 0.5
    threshold = 1  # Adjust this value based on your requirement
    pwd = os.getcwd()
    process_point_cloud(pwd + "/point_cloud_data/_point_cloud.ply", threshold, bin_size)
