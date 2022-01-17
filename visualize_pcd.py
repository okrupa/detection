import open3d as o3d
import numpy as np
import sys
import time

import copy

<<<<<<< HEAD
=======
from cv2 import destroyWindow
from open3d import visualization
import threading
def start_thread(func, name=None, args = []):
    threading.Thread(target=func, name=name, args=args).start()

>>>>>>> cmd-program-read-rosbagfile
def show_pcd(pcd_file):
    print("Load a ply point clouds, print them, and render them")
    pcd = o3d.io.read_point_cloud(pcd_file)
    print(pcd)
    print(np.asarray(pcd.points))
    #pcd.colors = o3d.Vector3dVector([1,1,1])
    o3d.visualization.draw_geometries([pcd])


def createWindow(window_name="MainWindow"):
    window = o3d.visualization.Visualizer()
    window.create_window(window_name=window_name, width=960, height=540, left=0, top=0)
    return window


def show_pcd_1(pcd_file, window_name="MainWindow"):

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='MainWindow', width=960, height=540, left=0, top=0)

    pcd = o3d.io.read_point_cloud(pcd_file[0])
    vis.add_geometry(pcd)
    vis.run()

    vis.destroy_window()
    vis.close()
#     start_thread(cos, args =[pcd_file])
# def cos(pcd_file):
#     visualization.gui.Application.instance.initialize()
#     w = o3d.visualization.O3DVisualizer("03DVisualizer", 640, 480)
#     visualization.gui.Application.instance.add_window(w)
#     # visualization.gui.Application.instance.add_window(w)
#     # material = o3d.visualization.rendering.Material()
#     pcd = o3d.io.read_point_cloud(pcd_file[0])
#     w.add_geometry("0", pcd)  # flower is a point cloud
#     w.reset_camera_to_default()
#     visualization.gui.Application.instance.run()
#     visualization.gui.Application.instance.quit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        rosbag = sys.argv[1]
    print(rosbag)
    show_pcd_1(rosbag)


def show(pcd_files):
    # vis = o3d.visualization.Visualizer()
    # vis.create_window(window_name='MainWindow', width=960, height=540, left=0, top=0)
    #
    # for i in range(0,len(pcd_files)):
    #     vis.clear_geometries()
    #     pcd = o3d.io.read_point_cloud(pcd_files[i][0])
    #     vis.add_geometry(pcd)
    #     vis.poll_events()
    #     vis.update_renderer()
    #     # time.sleep(1)
    # vis.destroy_window()

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name='MainWindow', width=960, height=540, left=0, top=0)

    for i in range(0, len(pcd_files)):
        vis.clear_geometries()
        pcd = o3d.io.read_point_cloud(pcd_files[i])
        vis.add_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()
        time.sleep(2)
    vis.destroy_window()
    vis.close()

    # vis = o3d.visualization.O3DVisualizer()
    # vis.create_window(window_name='MainWindow', width=960, height=540, left=0, top=0)
    #
    # for i in range(0, len(pcd_files)):
    #     vis.clear_geometries()
    #     pcd = o3d.io.read_point_cloud(pcd_files[i])
    #     vis.add_geometry(pcd)
    #     vis.poll_events()
    #     vis.update_renderer()
    #     time.sleep(2)
    # # vis.destroy_window()
    # # vis.close()
    # destroyWindow(vis)
    #
    # # visualization.gui.Application.instance.initialize()
    # w = o3d.visualization.O3DVisualizer("03DVisualizer", 640, 480)
    # visualization.gui.Application.instance.add_window(w)
    # w.show_axes = True
    # # material = o3d.visualization.rendering.Material()
    # w.add_geometry("0", pcd_files[0])  # flower is a point cloud
    # w.show()
    # # visualization.gui.Application.instance.run()
    #
    # # for i in range(1, len(pcd_files)):
    # #     vis.clear_geometries()
    # #     pcd = o3d.io.read_point_cloud(pcd_files[i])
    # #     vis.add_geometry(pcd)
    # #     vis.poll_events()
    # #     vis.update_renderer()
    # #     time.sleep(2)

def show_pcd_1_test(pcd_file, window_name="MainWindow"):

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pcd = o3d.io.read_point_cloud(pcd_file[0])
    mesh_r = copy.deepcopy(pcd)
    mesh_r.rotate(pcd.get_rotation_matrix_from_xyz((np.pi/ 1.9, np.pi , np.pi /4.5)),
                  center=(0, 0, 0))
    vis.add_geometry(mesh_r)
    ctr = vis.get_view_control()
    ctr.change_field_of_view(step=50)
    print("Field of view (before changing) %.2f" % ctr.get_field_of_view())
    vis.run()
    vis.destroy_window()