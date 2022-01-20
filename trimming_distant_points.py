import numpy as np
import math
import open3d as o3d
import visualize_pcd


def calculate_dist_between_two_points(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def get_max_distance(points, other):
    max_dist = max(calculate_dist_between_two_points(coord[0], coord[1], other[0], other[1]) for coord in points)
    return max_dist


def trim_distant_points(points, other, ratio=0.75):
    points_to_del = []
    max_dist = get_max_distance(points, other)
    print(f"Max distance: {max_dist}")
    for i, coord in enumerate(points):
        if(calculate_dist_between_two_points(coord[0], coord[1], other[0], other[1]) > ratio * max_dist):
            points_to_del.append(i)
    points = np.delete(points, points_to_del, 0)
    return points


def delete_algorithim(points):

    points_to_del = []
    for i, coord in enumerate(points):
        if coord[1] > 0:
             points_to_del.append(i)
        if coord[0] > 0:
             points_to_del.append(i)
    points = np.delete(points, points_to_del, 0)
    return points

def trim_points(points_bef):
    # points_after = delete_algorithim(points_bef)
    other = [0, 0]
    ratio = 0.3
    points_after = trim_distant_points(points=points_bef, other=other, ratio=ratio)
    return points_after



if __name__ == '__main__':

    pcd_load = o3d.io.read_point_cloud("1581791723.233274624.pcd")
    points_bef = np.asarray(pcd_load.points)
    other = [0, 0]
    ratio = 0.3

    points_after = trim_distant_points(points=points_bef, other=other, ratio=ratio)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_after)
    o3d.io.write_point_cloud("1581791723.233274624-trimmed.pcd", pcd)

    visualize_pcd.show_pcd("1581791723.233274624.pcd")
    visualize_pcd.show_pcd("1581791723.233274624-trimmed.pcd")
