import numpy as np
import math
import open3d as o3d
import visualize_pcd


def trim_far_points(points, dist=None):
    points_to_del = []
    for i, coord in enumerate(points):
        if math.sqrt(pow(coord[0], 2) + pow(coord[1], 2)) > dist:
            points_to_del.append(i)
    points = np.delete(points, points_to_del, 0)
    return points


"""if __name__ == '__main__':
    pcd_load = o3d.io.read_point_cloud("1581791678.433744128.pcd")
    points_bef = np.asarray(pcd_load.points)
    points_after = trim_far_points(points_bef, 11)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_after)
    o3d.io.write_point_cloud("1581791678.433744128-trimmed.pcd", pcd)

    visualize_pcd.show_pcd("1581791678.433744128.pcd")
    visualize_pcd.show_pcd("1581791678.433744128_trimmed.pcd")"""