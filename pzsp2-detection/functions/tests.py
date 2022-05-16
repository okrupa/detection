import unittest
import open3d as o3d
import numpy as np
import sys
sys.path.append('../')
from functions.detection import ObjectDetection
from functions.ransac2 import if_collinear, choose_points, ransac_algorithim
from functions.trimming_distant_points import calculate_dist_between_two_points, get_max_distance, set_ratio, trim_distant_points, trim_points


class Testclass(unittest.TestCase):
    
    def test_non_collinear_points(var):
        # A = (6,7,1), B = (2,−3,1), C = (4,−5,0) are non collinear points
        non_coll_points = [(6, 7, 1), (2, -3, 1), (4, -5, 0)]
        var.assertEqual(if_collinear(non_coll_points), False, "Should be False")


    def test_collinear_points(var):
        # A = (-1,0,2), B = (1,1,4), C = (3,2,6) are collinear points
        coll_points = [(-1, 0, 2), (1, 1, 4), (3, 2, 6)]
        var.assertEqual(if_collinear(coll_points), True, "Should be True")


    def test_find_collinear_points(var):
        # first three points together are collinear, but other of them combination is not
        # so choose_points should return non collinear points
        points = [(6, 7, 1), (2, -3, 1), (4, -5, 0), (-1, 0, 2)]
        non_coll = choose_points(points)
        var.assertEqual(if_collinear(non_coll), False, "Should be False")


    def test_read_pointcloud(var):
            pcd_load = o3d.io.read_point_cloud("1581791723.233274624.pcd")
            var.assertEqual(type(pcd_load), o3d.geometry.PointCloud, "Should be True")


    def test_set_ratio(var):
        ratio = set_ratio()
        var.assertTrue(type(ratio), float)


    def test_calculate_dist_between_points(var):
        point = [3, 4]
        other = [0, 0]
        var.assertEqual(calculate_dist_between_two_points(*point, *other), 5)
        var.assertTrue(calculate_dist_between_two_points(*other, *other) >= 0)


    def test_get_max_distance(var):
        points = [[3, 4], [1, 2]]
        other = [0, 0]
        var.assertEqual(get_max_distance(points, other), 5)
        var.assertFalse(get_max_distance(points, other) < 0)


    def test_trim_distant_points(var):
        pcd_load = o3d.io.read_point_cloud("1581791723.233274624.pcd")
        points_bef = np.asarray(pcd_load.points)
        other = [0, 0]
        ratio = 0.3
        points_after = trim_distant_points(points_bef, other, ratio)
        var.assertTrue(points_bef.size > points_after.size)


    def test_trim_points(var):
        pcd_load = o3d.io.read_point_cloud("1581791723.233274624.pcd")
        points_bef = np.asarray(pcd_load.points)
        ratio = 0.3
        points_after = trim_points(points_bef, ratio)
        var.assertTrue(points_bef.size > points_after.size)


    def test_ransac_algorithm(var):
        pcd_load = o3d.io.read_point_cloud("1581791723.233274624.pcd")
        points_bef = np.asarray(pcd_load.points)
        points_after = ransac_algorithim(points_bef)
        var.assertTrue(points_bef.size > points_after.size)


    def test_detection_do_dbscan(var):
        infile = "1581791723.233274624.pcd"
        eps = 0.2
        min_points = 40
        od = ObjectDetection(infile, eps, min_points)
        pcd, labeled_points, unique_labels = od.do_dbscan()
        var.assertEqual(type(pcd), o3d.geometry.PointCloud, "Should be True")
        var.assertTrue(len(labeled_points.keys()) > 0)
        for key in labeled_points:
            var.assertTrue(len(labeled_points[key]) >= 40)
        var.assertTrue(len(unique_labels) > 0)

        # def test_select_object_in_frame(var):
        #     infile = "1581791723.233274624.pcd"
        #     eps = 0.21
        #     min_points = 15
        #     od = ObjectDetection(infile, eps, min_points)
        #     pcd, labeled_points, unique_labels = od.do_dbscan()
        #     soif = SelectingObjectsInFrames(pcd, labeled_points, unique_labels)
        #     pcd_framed, obb_coords = soif.select_objects_in_frames(save=None)
        #     for obb in obb_coords:
        #         var.assertEqual(type(obb), o3d.geometry.Geometry3D)
        #     var.assertEqual(type(pcd_framed), o3d.geometry.PointCloud, "Should be True")


if __name__ == "__main__":
    unittest.main()