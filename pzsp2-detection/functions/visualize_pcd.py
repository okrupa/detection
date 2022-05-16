import open3d as o3d
import numpy as np
import time
from multiprocessing import Process
import copy


#Wywietlenie pliku pcd
def show_pcd_1(pcd_file):
    def f(pcd_file):
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name='MainWindow', width=960, height=540, left=0, top=0)

        pcd = o3d.io.read_point_cloud(pcd_file[0])
        vis.add_geometry(pcd)
        vis.run()

        vis.destroy_window()

    p = Process(target=f, args=(pcd_file,))
    p.start()
    p.join()


#
# def show_pcd(pcd_file):
#     print("Load a ply point clouds, print them, and render them")
#     pcd = o3d.io.read_point_cloud(pcd_file)
#     print(pcd)
#     print(np.asarray(pcd.points))
#     #pcd.colors = o3d.Vector3dVector([1,1,1])
#     o3d.visualization.draw_geometries([pcd])


# def show_pcd_1_test(pcd_file, window_name="MainWindow"):
#
#     vis = o3d.visualization.Visualizer()
#     vis.create_window()
#     pcd = o3d.io.read_point_cloud(pcd_file[0])
#     mesh_r = copy.deepcopy(pcd)
#     mesh_r.rotate(pcd.get_rotation_matrix_from_xyz((np.pi/ 1.9, np.pi , np.pi /4.5)),
#                   center=(0, 0, 0))
#     vis.add_geometry(mesh_r)
#     ctr = vis.get_view_control()
#     ctr.change_field_of_view(step=50)
#     print("Field of view (before changing) %.2f" % ctr.get_field_of_view())
#     vis.run()
#     vis.destroy_window()

#
# def show(pcd_files):
#
#     vis = o3d.visualization.Visualizer()
#     vis.create_window(window_name='MainWindow', width=960, height=540, left=0, top=0)
#
#     for i in range(0, len(pcd_files)):
#         vis.clear_geometries()
#         pcd = o3d.io.read_point_cloud(pcd_files[i])
#         vis.add_geometry(pcd)
#         vis.poll_events()
#         vis.update_renderer()
#         time.sleep(2)
#     vis.destroy_window()
#     vis.close()

