from cv2 import destroyWindow
import visualize_pcd
import get_data
import choose_pcd
import dbscan
from delete_files import delete_files_in_directory
from ransac2 import ransac_algorithim
import numpy as np
import open3d as o3d
import os
import glob
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from trimming_distant_points import trim_points
from detection import detection

CONST_DIR = os.getcwd() + os.sep + "results"

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def save_file(pcd):
    root = Tk()
    root.withdraw()
    dir = askdirectory(title='Choose a directory')
    root.destroy()
    filename = input("Enter file name: ")
    last_chars = filename[-4:]
    if last_chars != '.pcd':
        filename = filename + '.pcd'
    filename = dir + '/' + filename
    o3d.io.write_point_cloud(filename, pcd)
    return filename

def unpack_rosbag():
    root = Tk()
    root.withdraw()
    file = askopenfilename()
    print(file)
    root.destroy()
    if os.path.isfile(file):
        print("ok")
    print(file[-4:])
    if os.path.isfile(file) and file[-4:] == ".bag":
        get_data.get_data_from_rosbag(file, CONST_DIR)
        return True
    return False

def visualize_file():
    root = Tk()
    root.withdraw()
    file = askopenfilename()
    root.destroy()
    visualize_pcd.show_pcd_1([file])

def detect():
    root = Tk()
    root.withdraw()
    file = askopenfilename(title='Choose a file')
    root.destroy()
    # file = "/home/kolga/Desktop/testpzsp2/pzsp2/pcd_files/1581791678.433744128.pcd"
    if len(file) != 0:
        pcd_load = o3d.io.read_point_cloud(file)
        points_bef = np.asarray(pcd_load.points)

        points_trim = trim_points(points_bef)

        points_after = ransac_algorithim(points_trim)
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_after)
        path = CONST_DIR + os.sep + "pcd_files"
        if not os.path.isdir(path):
            os.mkdir(path)
        o3d.io.write_point_cloud(path, pcd)

        folder = CONST_DIR + os.sep + "results"
        if not os.path.exists(folder):
            os.mkdir(folder)
        dbscan.do_dbscan(path)
        file_s = file.split("/")
        f = file_s[-1]
        file_dbscan = os.path.abspath(folder + os.sep + f[:-4] + "-ransac-result.pcd")
        visualize_pcd.show_pcd_1([file_dbscan])


def detect_list(files):
    folder = CONST_DIR + os.sep + "ransac_files"
    if os.path.exists(folder):
        delete_files_in_directory(folder)
    else:
        os.mkdir(folder)
    for i, file in enumerate(files):
        pcd_load = o3d.io.read_point_cloud(file)
        points_bef = np.asarray(pcd_load.points)
        points_trim = trim_points(points_bef)

        points_after = ransac_algorithim(points_trim)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_after)
        file_name = folder + f"/points{i}.pcd"
        o3d.io.write_point_cloud(file_name, pcd)
    path_pcd = CONST_DIR + os.sep + "ransac_files"
    p_pcd = path_pcd + "/*.pcd"
    pcd = [f for f in glob.glob(p_pcd)]
    pcd.sort()
    return pcd


def visualize_obstacle():
    print("Visualize obstacle not implemented yet")

# def detect_obstacle(pcd_list):
#
#     for p in pcd_list:
#         detect_and_show_obstacle(p):

def get_interval():
    DIR = CONST_DIR + os.sep + "pointclouds"
    ext_files_num = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    while True:
        interval = input(
            f"Insert desired interval (number of iterations) between displaying extracted point clouds {ext_files_num}:")
        is_int = all(i.isdigit() for i in interval)
        if is_int:
            if int(interval) <= ext_files_num or int(interval) >= 1:
                return int(interval)
            else:
                while True:
                    next = input(f"Invalid input, do you want to re-enter the value?\nYes - y\nNo -n\n")
                    if next == 'n' or next == 'y':
                        break
                if next == 'n':
                    return -1
        else:
            while True:
                next = input(f"Invalid input, do you want to re-enter the value?\n Yes - y\nNo -n")
                if next == 'n' or next == 'y':
                    break
            if next == 'n':
                return -1


def run_algorithm():
    # unpack = unpack_rosbag()
    unpack = True
    if unpack:
        interval = get_interval()
        if interval == -1:
            return
        else:
            output = choose_pcd.get_sequence(interval, CONST_DIR)
            if output is not None:
                print("Run ransac")
                ransac_output = detect_list(output)
                print("Get results")

                # folder = CONST_DIR + os.sep +"results"
                # if os.path.exists(folder):
                #     delete_files_in_directory(folder)
                # else:
                #     os.mkdir(folder)

                for i in ransac_output:
                    detection(i)

            else:
                print("Error while choosing file. Make sure that bag file unpacked correctly.")
    else:
        print("Wrong file")

def get_first_message():
    # unpack = unpack_rosbag()
    unpack = True
    if unpack:
        output = choose_pcd.get_first(CONST_DIR)
        if output is not None:

            print("Run ransac")
            ransac_output = detect_list(output)
            print("Get results")

            # folder = CONST_DIR + os.sep + "results"
            # if os.path.exists(folder):
            #     delete_files_in_directory(folder)
            # else:
            #     os.mkdir(folder)

            for i in ransac_output:
                detection(i)

        else:
            print("Error while choosing file. Make sure that bag file unpacked correctly.")
    else:
        print("Wrong file")


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
    print(f'The default folder for saving files is currently: {CONST_DIR}')
    answer = input("Would you like to change it? (y/n) ")
    if answer == 'y':
        root = Tk()
        root.withdraw()
        CONST_DIR = askdirectory(title='Choose a directory')
        root.destroy()
    else:
        if not os.path.isdir(CONST_DIR):
            os.mkdir(CONST_DIR)
        # else:
        #     delete_files_in_directory(CONST_DIR)
    program_menu()
