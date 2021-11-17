import pyransac3d as pyrsc
import numpy as np
import open3d as o3d

pcd_load = o3d.io.read_point_cloud("pyransac3d/point_cloud_data/1581791678.433744128.pcd")
# pcd_load = o3d.io.read_point_cloud("pyransac3d/point_cloud_data/cloud_bin_0.pcd")
points = np.asarray(pcd_load.points)
print(points)

sph = pyrsc.Sphere()
center, radius, inliers = sph.fit(points, thresh=0.4)
print(f"center: \t{center} \nradius: \t{radius} \ninliers: \t{inliers}")
