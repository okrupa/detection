import os
import glob
import numpy as np
import open3d as o3d
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from cv2 import destroyWindow
import subprocess
import cloud_trimming
import visualize_pcd
import get_data
import choose_pcd
import dbscan
from delete_files import delete_files_in_directory
from ransac2 import ransac_algorithim


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def unpack_rosbag():
    root = Tk()
    root.withdraw()
    file = askopenfilename()
    root.destroy()

    if len(file) != 0:
        get_data.get_data_from_rosbag(file)

def visualize_file():

    root = Tk()
    root.withdraw()
    file = askopenfilename()
    root.destroy()
    visualize_pcd.show_pcd_1([file])


def detect():
    # root = Tk()
    # root.withdraw()
    # file = askopenfilename(title='Choose a file')
    # root.destroy()
    file = "/home/kolga/Desktop/testpzsp2/pzsp2/pcd_files/1581791678.433744128.pcd"
    if len(file) != 0:
        pcd_load = o3d.io.read_point_cloud(file)
        points_bef = np.asarray(pcd_load.points)
        # TODO: 
        # trimming distant points (from the center)
        #points_after_trimming = cloud_trimming.trim_far_points(points_bef, 11) 
        points_after = ransac_algorithim(points_bef)    # => points_after = ransac_algorithim(points_after_trimming)
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
        visualize_pcd.show_pcd_1([file_dbscan])


def detect_list(files):
    folder = "ransac_files"
    if os.path.exists(folder):
        delete_files_in_directory(folder)
    else:
        os.mkdir(folder)
    for i, file in enumerate(files):
        print(f"file")
        pcd_load = o3d.io.read_point_cloud(file)
        points_bef = np.asarray(pcd_load.points)
        points_after = ransac_algorithim(points_bef)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_after)
        o3d.io.write_point_cloud(f"ransac_files/points{i}.pcd", pcd)
    cwd = os.path.abspath(os.getcwd())
    path_pcd = os.path.join(cwd, folder)
    p_pcd = path_pcd + "/*.pcd"
    pcd = [f for f in glob.glob(p_pcd)]
    pcd.sort()
    return pcd


def visualize_obstacle():
    print("Visualize obstacle not implemented yet")


def run_algorithm():
    unpack_rosbag()
    output = choose_pcd.get_sequence(150)

    if output is not None:

        print("Run ransac")
        ransac_output = detect_list(output)
        print("Get results")

        folder = "results"
        if os.path.exists(folder):
            delete_files_in_directory(folder)
        else:
            os.mkdir(folder)

        for i in ransac_output:
            dbscan.do_dbscan(i)

        cwd = os.path.abspath(os.getcwd())
        path_pcd = os.path.join(cwd, "results")
        p_pcd = path_pcd + "/*.pcd"
        pcd = [f for f in glob.glob(p_pcd)]
        pcd.sort()

        visualize_pcd.show(pcd)

    else:
        print("Error while choosing file. Make sure that bag file unpacked correctly.")


def get_first_message():
    unpack_rosbag()
    output = choose_pcd.get_first()
    if output is not None:

        print("Run ransac")
        ransac_output = detect_list(output)
        print("Get results")

        folder = "results"
        if os.path.exists(folder):
            delete_files_in_directory(folder)
        else:
            os.mkdir(folder)

        for i in ransac_output:
            dbscan.do_dbscan(i)

        cwd = os.path.abspath(os.getcwd())
        path_pcd = os.path.join(cwd, "results")
        p_pcd = path_pcd + "/*.pcd"
        pcd = [f for f in glob.glob(p_pcd)]
        pcd.sort()

        visualize_pcd.show_pcd_1(pcd)

    else:
        print("Error while choosing file. Make sure that bag file unpacked correctly.")


def number_to_func(argument):
    try:
        argument = int(argument)
    except ValueError:
        print("Invalid input. Input should be a number.")
        return
    switcher = {
        1: unpack_rosbag,
        2: visualize_file,
        3: detect,
        4: visualize_obstacle,
        5: run_algorithm,
        6: get_first_message
    }
    func = switcher.get(argument, lambda: "Invalid number")
    func()


def program_menu():
    clearConsole()
    while True:
        print("Menu")
        print("1. Unpack rosbag")
        print("2. Visualize pcd file")
        print("3. Detect obstacle")
        print("4. Visualize obstacle on image")
        print("5. Run algorithm")
        print("6. Get first message from rosbag file")
        print("7. Exit")
        number = input("Choose what would you like to do (1-7): ")
        print(f"You chose number {number}")
        if number == "7":
            quit()
        number_to_func(number)

           
if __name__ == "__main__":
    program_menu()
