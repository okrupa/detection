import random
import numpy as np
from sympy import Point
import pyransac3d as pyrsc
import open3d as o3d
import visualize_pcd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def if_collinear(points):
    '''
    Czy punkty definiują płaszczyznę
    '''
    p1, p2, p3 = Point(points[0]), Point(points[1]), Point(points[2])
    return Point.is_collinear(p1, p2, p3)

def choose_points(points):
    '''
    Wybierz w sposób losowy trzy punkty spośród punktów zawartych w chmurze.
    Jeśli wybrane punkty nie definiują w sposób jednoznaczny płaszczyzny (tzn.
    są współliniowe), wybierz inne trzy punkty. 
    '''
    collinear = True
    while collinear:
        chosen_points = random.choices(points, k=3)
        for i in range(len(chosen_points)):
            chosen_points[i] = np.array(chosen_points[i])
        collinear = if_collinear(chosen_points)
    chosen_points = np.array(chosen_points)
    return chosen_points

def ransac_algorithim(points):
    plane = pyrsc.Plane()
    min_points_amount = len(points) * 0.3
    while min_points_amount < len(points):
        chosen_points = choose_points(points)
        '''
        Oblicz równanie płaszczyzny pasującej do wybranych punktów, tzn. wyznacz
        współczynniki a, b, c, d występujące w równaniu ax + by + cd + d = 0. 
        '''
        plane_abcd, inliers = plane.fit(chosen_points, thresh = 0.01, maxIteration = 100)
        if plane_abcd:
            a, b, c, d = plane_abcd
            points_to_del = []
            for i, coord in enumerate(points):
                '''
                Policz liczbę punktów pasujących do znalezionego modelu. Punkt jest uznawany
                za pasujący (ang. inlier), jeśli jego odległość od płaszczyzny nie przekracza
                określonej wcześniej wartości tolerancji δ. 
                '''
                dist = np.abs(a*coord[0]+b*coord[1]+c*coord[2]+d) / np.sqrt(a**2+b**2+c**2)
                if dist < 0.01:
                    points_to_del.append(i)
        points = np.delete(points, points_to_del, 0)
    return points

def unpack_rosbag():
    print("Unpack rosbag not implemented yet")

def visualize_file():
    Tk().withdraw()
    file = askopenfilename()
    visualize_pcd.show_pcd(file)

def detect():
    Tk().withdraw()
    file = askopenfilename()
    pcd_load = o3d.io.read_point_cloud(file)
    points_bef = np.asarray(pcd_load.points)
    points_after = ransac_algorithim(points_bef)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_after)
    o3d.io.write_point_cloud("result_points.pcd", pcd)

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
