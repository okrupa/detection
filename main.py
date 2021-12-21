from ransac import ransac
import visualize_pcd
import open3d as o3d
import time
import sys
import numpy as np
from matplotlib import pyplot as plt


if __name__ == "__main__":
    '''
    Running ransac algorithm for given pcd file,
    which returns result pcd and shows both on screen
    '''

    #RANSAC
    delta = float(sys.argv[1]) if len(sys.argv) > 1 else 0.01
    points = ransac(pcd_file="pcd/1581791688.333029376.pcd", delta_val=0.01)      
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud("pcd/1581791688.333029376_delta_val=0.01.pcd", pcd)           

    # without windows  
    visualize_pcd.show_pcd("pcd/1581791688.333029376.pcd")                         
    visualize_pcd.show_pcd("pcd/1581791688.333029376_delta_val=0.01.pcd") 
    
    # visualization with windows - FIX
    #visualize_pcd.show_pcd_1("1581791688.333029376.pcd", "MainWindow")   
    #time.sleep(1)                      
    #visualize_pcd.show_pcd_1("1581791688.333029376_delta_val=0.005.pcd", "SecondWindow")   
     


    
