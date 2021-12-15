import visualize_pcd
import get_data
from ransac2 import ransac_algorithim
import numpy as np
import open3d as o3d
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def unpack_rosbag():
    print("Unpack rosbag not implemented yet")
    Tk().withdraw()
    file = askopenfilename()
    
    if  len(file) != 0:
    	get_data.get_data_from_rosbag(file)

def visualize_file():
    Tk().withdraw()
    file = askopenfilename()

    if  len(file) != 0:
    	visualize_pcd.show_pcd(file)

def detect():
    Tk().withdraw()
    file = askopenfilename()
    if  len(file) != 0:
    	
	pcd_load = o3d.io.read_point_cloud(file)
	points_bef = np.asarray(pcd_load.points)
	points_after = ransac_algorithim(points_bef)
	pcd = o3d.geometry.PointCloud()
	pcd.points = o3d.utility.Vector3dVector(points_after)
	o3d.io.write_point_cloud("pcd_files/result_points.pcd", pcd)

def visualize_obstacle():
    print("Visualize obstacle not implemented yet")

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
        4: visualize_obstacle
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
        print("5. Exit")
        number = input("Choose what would you like to do (1-5): ")
        print(f"You chose number {number}")
        if number == "5":
            quit()
        number_to_func(number)

           
if __name__ == "__main__":
    program_menu()
