
import visualize_pcd
import get_data
import choose_pcd
import dbscan
from delete_files import delete_files_in_directory
from ransac2 import ransac_algorithim, delete_algorithim
import numpy as np
import open3d as o3d
import os
import glob
from tkinter import Tk
from tkinter.filedialog import askopenfilename
def detect():
    # root = Tk()
    # root.withdraw()
    # file = askopenfilename(title='Choose a file')
    # root.destroy()
    file = "/home/kolga/Desktop/testpzsp2/prog/pcd_files/1581791678.433744128.pcd"
    if len(file) != 0:
        pcd_load = o3d.io.read_point_cloud(file)
        points_bef = np.asarray(pcd_load.points)
        points_after = ransac_algorithim(points_bef)
        points_after = delete_algorithim(points_after)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_after)
        file_s = file.split("/")
        f = file_s[-1]
        filename = "pcd_files/" + f[:-4] + "-ransac.pcd"
        o3d.io.write_point_cloud(filename, pcd)
        folder = "results"
        if not os.path.exists(folder):
            os.mkdir(folder)

        dbscan.do_dbscan(os.getcwd() + "/"+filename)
        file_dbscan = os.path.abspath(os.getcwd()+"/results/" + f[:-4] + "-ransac-result.pcd")
        visualize_pcd.show_pcd_1_test([file_dbscan])

detect()
