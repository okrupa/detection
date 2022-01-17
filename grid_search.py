import open3d as o3d

import visualize_pcd
from detection import ObjectDetection, SelectingObjectsInFrames

'''
Results: (not cut)
- e=0.2, min_points=35 -> 47 
- e=0.2, min_points=40 -> 39
- e=0.21, min_points=40 -> 34 

(cut):
- e=0.2, min_points=20 -> 23
- e=0.2, min_points=15 -> 41 
- e=0.21, min_points=25 -> 23
- e=0.21, min_points=15 -> 42 (chosen)
'''

if __name__ == "__main__":
                                          
    eps = [0.2, 0.21, 0.22, 0.23]
    min_points = [40, 35, 30, 25, 20, 15] 

    for e in eps:
        for min_point in min_points:
            #infile = "1581791678.433744128_trimmed_result.pcd"
            infile = "1581791678.433744128-ransac.pcd"
            od = ObjectDetection(infile, e, min_point)
            print("EPSILON: ", e, "\nMIN_POINTS: ", min_point)

            pcd, labeled_points, unique_labels = od.do_dbscan()
            soif = SelectingObjectsInFrames(pcd, labeled_points, unique_labels)
            pcd_framed = soif.select_objects_in_frames()

            o3d.io.write_point_cloud('1581791678.433744128_ransac' + str(e) + '_' + str(min_point) + '.pcd', pcd)
            visualize_pcd.show_pcd('1581791678.433744128_ransac' + str(e) + '_' + str(min_point) + '.pcd')
















'''
Example grid search done for "1581791688.333029376.pcd"
'''

"""if __name__ == '__main__':
    results = ["pcd/1581791688.333029376_delta_val=0.001.pcd",
                "pcd/1581791688.333029376_delta_val=0.002.pcd",
                "pcd/1581791688.333029376_delta_val=0.005.pcd",
                "pcd/1581791688.333029376_delta_val=0.01.pcd",
                "pcd/1581791688.333029376_delta_val=0.05.pcd",
                "pcd/1581791688.333029376_delta_val=0.1.pcd",
                "pcd/1581791688.333029376_delta_val=0.5.pcd"]
    #ex_pcd = o3d.io.read_point_cloud("pcd/1581791723.233274624_result.pcd")
    for i in range(len(results)):
        #pcd = ex_pcd
        pcd = o3d.io.read_point_cloud(results[i])
        eps = [0.4]
        min_points = [40, 60]
        col_0 = []
        # eps = [0.2 * i for i in range(1, 8, 1)]
        # min_points = [20 * i for i in range(1, 6, 1)]
        for e in eps:
            for p in min_points:
                print(f"Epsilon: {e} \tMin number of points: {p}")
                with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
                    labels = np.array(pcd.cluster_dbscan(eps=e, min_points=p, print_progress=True))
                    cprint(f"Labels: {colored(labels, 'green', attrs=['bold'])}")
                    col_0.append(pcd[j] for j in range(labels.size) if labels[j] == 0)
                print(col_0)
                max_label = labels.max()
                cprint(f"Max label: {colored(max_label, 'green', attrs=['bold'])}")
                cprint(f"Point cloud has {colored(max_label + 1, 'green', attrs=['bold'])}")
                colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
                colors[labels < 0] = 0
                pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
                
                key_to_callback = {}
                vis = createWindow(window_name=results[i])
                key_to_callback[ord("C")] = destroyWindow(vis)
                o3d.visualization.draw_geometries_with_key_callbacks([pcd], key_to_callback, results[i])
                
                #o3d.visualization.draw_geometries([pcd],
                #                      zoom=0.455,
                #                      front=[-0.4999, -0.1659, -0.8499],
                #                      lookat=[2.1813, 2.0619, 2.0999],
                #                      up=[0.1204, -0.9852, 0.1215])"""