import pyransac3d as pyrsc
import numpy as np
import open3d as o3d

# pcd_load = o3d.io.read_point_cloud("pyransac3d/point_cloud_data/1581791678.433744128.pcd")
pcd_load = o3d.io.read_point_cloud("pyransac3d/point_cloud_data/cloud_bin_0.pcd")
points = np.asarray(pcd_load.points)
print(points)

plane1 = pyrsc.Plane()
best_eq, best_inliers = plane1.fit(points, 0.01)
print(f"best_eq: \t{best_eq} \nbest_inliers: \t{best_inliers}")
