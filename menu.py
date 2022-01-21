import numpy as np
import open3d as o3d
import os
import glob
from tkinter import Tk
import shutil

from functions.visualize_pcd import show_pcd_1
from functions.get_data import get_data_from_rosbag
from functions.choose_pcd import get_first, get_sequence
from functions.delete_files import delete_files_in_directory
from functions.ransac2 import ransac_algorithim
from tkinter.filedialog import askopenfilename, askdirectory
from functions.trimming_distant_points import set_ratio, trim_points
from functions.detection import detection


CONST_DIR = os.getcwd() + os.sep + "results"


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def unpack_rosbag():
    root = Tk()
    root.title('Choose .bag file')
    root.withdraw()
    file = askopenfilename()
    root.destroy()
    if os.path.isfile(str(file)) and str(file)[-4:] == ".bag":
        get_data_from_rosbag(file, CONST_DIR)
        return True
    else:
        print("Invalid input")
    return False


def check_unpack_rosbag():
    pcl = CONST_DIR + os.sep + "pointclouds"
    img = CONST_DIR + os.sep + "images"
    if os.path.isdir(pcl) or os.path.isdir(img):
        while True:
            delete = input("Folder in witch pcd files and images files will be saved already exist. DO you want to delete these folders content and unpack .bag date to these folders?\nYes-y\nNo-n\n")
            if delete.isalpha():
                if delete == 'y' :
                    if os.path.isdir(pcl):
                        shutil.rmtree(pcl)
                    if os.path.isdir(img):
                        shutil.rmtree(img)
                    unpack_rosbag()
                    return
                elif delete =='n':
                    return
                else:
                    print(f"Invalid input\n")
            else:
                print(f"Invalid input\n")
    else:
        unpack_rosbag()


def visualize_file():
    root = Tk()
    root.withdraw()
    file = askopenfilename()
    root.destroy()
    if os.path.isfile(str(file)) and str(file)[-4:] == ".pcd":
        show_pcd_1([str(file)])
    else:
        print("Wrong input file")


def detect_list(files):
    folder = CONST_DIR + os.sep + "ransac_files"
    if os.path.exists(folder):
        delete_files_in_directory(folder)
    else:
        os.mkdir(folder)
    ratio = set_ratio()
    for i, file in enumerate(files):
        print(file)
        pcd_load = o3d.io.read_point_cloud(file)
        points_bef = np.asarray(pcd_load.points)
        points_trim = trim_points(points_bef, ratio)
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
    root = Tk()
    root.withdraw()
    file = askopenfilename()
    root.destroy()
    if os.path.isfile(str(file)) and str(file)[-4:] == ".pcd":
        detection(str(file), False)
    else:
        print("Wrong input file")


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
    pcl = CONST_DIR + os.sep + "pointclouds"
    img = CONST_DIR + os.sep + "images"
    if os.path.isdir(pcl) and os.path.isdir(img):

        interval = get_interval()
        if interval == -1:
            return
        else:
            output = get_sequence(interval, CONST_DIR)
            if output is not None:
                print("Run ransac")
                ransac_output = detect_list(output)
                print("Get results")

                for i in ransac_output:
                    detection(i, True)
            else:
                print("Error while choosing file. Make sure that bag file unpacked correctly.")
    else:
        print("Please get the data from the .bag file first and make sure that bag file unpacked correctly.\n")


def extract_and_run_algorithm():
    unpack = unpack_rosbag()

    if unpack:
        interval = 100
        output = get_sequence(interval, CONST_DIR)
        if output is not None:
            print("Run ransac")
            ransac_output = detect_list(output)
            print("Get results")

            for i in ransac_output:
                detection(i, True)

        else:
            print("Error while choosing file. Make sure that bag file unpacked correctly.")
    else:
        print("Wrong file")


def extract_and_get_first_message():
    unpack = unpack_rosbag()
    if unpack:
        output = get_first(CONST_DIR)
        if output is not None:

            print("Run ransac for:")
            ransac_output = detect_list(output)
            print("Get results")

            for i in ransac_output:
                detection(i, True)

        else:
            print("Error while choosing file. Make sure that bag file unpacked correctly.")
    else:
        print("Wrong file")


def get_first_message():
    pcl = CONST_DIR + os.sep + "pointclouds"
    img = CONST_DIR + os.sep + "images"
    if os.path.isdir(pcl) and os.path.isdir(img):
        output = get_first(CONST_DIR)
        if output is not None:

            print("Run ransac for:")
            ransac_output = detect_list(output)
            print("Get results")

            for i in ransac_output:
                detection(i, True)

        else:
            print("Error while choosing file. Make sure that bag file unpacked correctly.")
    else:
        print("Please get the data from the .bag file first and make sure that bag file unpacked correctly.\n")


def number_to_func(argument):
    try:
        argument = int(argument)
    except ValueError:
        print("Invalid input. Input should be a number.")
        return
    switcher = {
        1: check_unpack_rosbag,
        2: run_algorithm,
        3: get_first_message,
        4: visualize_file,
        5: visualize_obstacle,
        6: extract_and_run_algorithm,
        7: extract_and_get_first_message
    }
    func = switcher.get(argument, lambda: "Invalid number")
    func()


def program_menu():
    clearConsole()
    while True:
        print("Menu")
        print("1. Unpack rosbag")
        print("2. Run algorithm (Get data from previously extracted .bag file, next get interval between displaying extracted point clouds and show detected obstacles")
        print("3. Get first message from rosbag file (Get data from previously extracted .bag file and show detected obstacle on first .pcd file")
        print("4. Visualize pcd file")
        print("5. Visualize obstacle on pcd file")
        print("6. Extract from .ros file and run algorithm (with interval=100 between displaying extracted point clouds), show detected obstacles")
        print("7. Extract .ros file and show detected obstacle on first .pcd file")
        print("8. Exit")
        number = input("Choose what would you like to do (1-8): ")
        print(f"You chose number {number}")
        if number == "8":
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
