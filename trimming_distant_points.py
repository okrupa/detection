from typing import Type
import numpy as np
import math
import open3d as o3d
import visualize_pcd


def ask_if_to_trim_points():
    ans = input("Do you want to trim distant points?\n[y/n]: ")
    return ans

def ask_about_ratio_to_trim_points():
    ans = input("How much distant points do you want to remove? \n[Legend: 0.2-close, 1-very distant, default=0.75]: ")
    return ans

def set_default_ratio():
    ratio = 0.75
    return ratio

def check_if_ratio_is_correct(ratio):
    if ratio > 0.2 and ratio <= 1:
        return ratio
    ratio = set_default_ratio()
    return ratio
    
def get_entered_ratio(ratio):
    try:
        ratio = float(ratio)
        check_if_ratio_is_correct(ratio)
    except TypeError:
        ratio = set_default_ratio()
    return ratio

def set_ratio():
    ans = ask_if_to_trim_points()
    if ans in ['Y', 'y']:
        ratio_ans = ask_about_ratio_to_trim_points()
        ratio = get_entered_ratio(ratio_ans)
    else:
        ratio = set_default_ratio()
    return ratio


def calculate_dist_between_two_points(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def get_max_distance(points, other):
    max_dist = max(calculate_dist_between_two_points(coord[0], coord[1], other[0], other[1]) for coord in points)
    return max_dist


def trim_distant_points(points, other, ratio):
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

def trim_points(points_bef, ratio):
    # points_after = delete_algorithim(points_bef)
    other = [0, 0]
    points_after = trim_distant_points(points=points_bef, other=other, ratio=ratio)
    return points_after




if __name__ == '__main__':

    # pcd_load = o3d.io.read_point_cloud("1581791723.233274624.pcd")
    # points_bef = np.asarray(pcd_load.points)
    # other = [0, 0]
    # ratio = 0.3

    # points_after = trim_distant_points(points=points_bef, other=other, ratio=ratio)
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(points_after)
    # o3d.io.write_point_cloud("1581791723.233274624-trimmed.pcd", pcd)

    # visualize_pcd.show_pcd("1581791723.233274624.pcd")
    # visualize_pcd.show_pcd("1581791723.233274624-trimmed.pcd")

    set_ratio()
