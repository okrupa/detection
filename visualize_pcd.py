import open3d as o3d
import numpy as np



def show_pcd(pcd_file):
    print("Load a ply point clouds, print them, and render them")
    pcd = o3d.io.read_point_cloud(pcd_file)
    print(pcd)
    print(np.asarray(pcd.points))
    #pcd.colors = o3d.Vector3dVector([1,1,1])
    o3d.visualization.draw_geometries([pcd])
    return True
