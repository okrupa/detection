import pyransac3d as pyrsc
import numpy as np
import open3d as o3d
import math

from sympy import Point


def random_sample(arr: np.array, size: int = 1) -> np.array:
    return arr[np.random.choice(len(arr), size=size, replace=False)]


def calculate_distance(point: np.array, best_eq: list) -> int:
    x, y, z = point
    a, b, c, d = best_eq
    nom = abs((a * x + b * y + c * z + d))
    denom = math.sqrt(a * a + b * b + c * c + d * d)

    distance = nom / denom
    return distance


def collinear(points):
    points_to_check = []
    assert points.ndim > 1, "Multiple points"
    for point in points:
        x, y, z = point
        points_to_check.append(Point(x, y, z))
    return Point.is_collinear(points_to_check[0], points_to_check[1], points_to_check[2])


def ransac(pcd_file, delta_val=0.01):
    best_inliers = 0
    best_eq = 0
    pcd_load = o3d.io.read_point_cloud(pcd_file)
    points = np.asarray(pcd_load.points)
    plane1 = pyrsc.Plane()
    min_points = int(len(points) / 3)

    loop = 0
    while len(points) > min_points:
        print("LOOP", loop, "Total points", len(points))
        loop += 1
        random_points = random_sample(points, 3)
        if collinear(random_points):
            continue
        best_eq, best_inliers = plane1.fit(
            random_points,
            delta_val,
            maxIteration=100
        )
        if not best_eq:
            continue

        to_delete = []
        for i, point in enumerate(points):
            dist = calculate_distance(point, best_eq)
            if dist < delta_val:
                to_delete.append(i)

        points = np.delete(points, to_delete, 0)
    return points


if __name__ == "__main__":
    import sys
    delta = float(sys.argv[1]) if len(sys.argv) > 1 else 0.01
    points = ransac(pcd_file="example.pcd", delta_val=delta)            # cloud_bin_0
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud("result.pcd", pcd)