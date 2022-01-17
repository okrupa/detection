import math
import time
import unittest

from detection import ObjectDetection, SelectingObjectsInFrames
from ransac2 import if_collinear, choose_points, ransac_algorithim


class Testclass(unittest.TestCase):

    def test_case_if_collinear(var):
        # A=(6,7,1), B=(2,−3,1), C=(4,−5,0) are non collinear points
        example_points = [(6, 7, 1), (2, -3, 1), (4, -5, 0)]
        var.assertEqual(if_collinear(example_points), False, "Should be False")

    def test_if_collinear2(var):
        # A=(-1,0,2), B=(1,1,4), C=(3,2,6) are collinear points
        example_points = [(-1, 0, 2), (1, 1, 4), (3, 2, 6)]
        var.assertEqual(if_collinear(example_points), True, "Should be True")
    
    def test_choosing_points_that_are_collinear(var):
        pass

    def test_ransac_algorithm(var):
        pass

    def test_detection(var):
        pass

    def test_selecting_object_in_frame(var):
        pass

    def test_frames_coordinates(var):
        pass

    def test_detection_time_with_ransac(var):
        pass

    def test_detection_time_without_ransac(var):
        pass

    def test_compare_time_detection(var):
        pass


if __name__ == "__main__":
    unittest.main()