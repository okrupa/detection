import numpy as np
import open3d as o3d


class ObjectDetection:

    def __init__(self, infile=None, eps=0.4, min_points=200):
        self.infile = infile
        self.pcd = None
        self.eps = eps
        self.min_points = min_points
        self.unique_labels = None
        self.labeled_points = {}

    def __str__(self):
        return 'Epsilon: {self.eps} \nMin number of points: {self.min_points}'.format(self=self)

    def do_dbscan(self):
        self.pcd = o3d.io.read_point_cloud(self.infile)
        with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(self.pcd.cluster_dbscan(eps=self.eps, min_points=self.min_points, print_progress=True))
            self.unique_labels = np.unique(np.array(labels))
            for unique in self.unique_labels:
                self.labeled_points[unique] = []
            for key in self.labeled_points.keys():
                for i in range(len(labels)):
                    if(labels[i] == key):
                        self.labeled_points[key].append(self.pcd.points[i])
        return self.pcd, self.labeled_points, self.unique_labels


class SelectingObjectsInFrames:

    def __init__(self, pcd=None, labeled_points=None, unique_labels=None):
        self.pcd = pcd
        self.pcd_framed = []
        self.labeled_points = labeled_points
        self.unique_labels = unique_labels

    def select_objects_in_frames(self):
        obb = []
        obb_coords = []
        self.pcd_framed.append(self.pcd)
        for i in range(len(self.unique_labels) - 1):
            pcd_ = o3d.geometry.PointCloud()
            pcd_.points = o3d.utility.Vector3dVector(self.labeled_points[i])
            obb = pcd_.get_oriented_bounding_box()
            obb_coords.append(np.asarray(obb.get_box_points()))
            self.pcd_framed.append(obb)
        o3d.visualization.draw_geometries(self.pcd_framed)
        return self.pcd_framed, obb_coords


if __name__ == "__main__":
    infile = "1581791678.433744128-result.pcd"
    eps = 0.4
    min_points = 40

    od = ObjectDetection(infile, eps, min_points)
    pcd, labeled_points, unique_labels = od.do_dbscan()
    soif = SelectingObjectsInFrames(pcd, labeled_points, unique_labels)
    pcd_framed, obb_coords = soif.select_objects_in_frames()
    # print(obb_coords)                                           # frames coords - 8 points for each frame
