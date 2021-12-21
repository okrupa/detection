import visualize_pcd
from termcolor import colored, cprint
import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d


def do_dbscan(infile, eps=0.4, min_points=40):
    pcd = o3d.io.read_point_cloud(infile)
    print(pcd)
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug):
        labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))
        cprint(f"Labels: {colored(labels, 'green', attrs=['bold'])}")
    max_label = labels.max()
    # cprint(f"Max label: {colored(max_label, 'green', attrs=['bold'])}")
    cprint(f"Point cloud has {colored(max_label + 1, 'green', attrs=['bold'])}")
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    outfile = save_pcd_to_file(pcd, infile)
    return outfile


def save_pcd_to_file(pcd, file):
    filename = file[:-4] + "-result.pcd"
    print(filename)
    o3d.io.write_point_cloud(filename, pcd)
    return filename


if __name__ == "__main__":
    infile = "1581791723.233274624.pcd"                  # point cloud file before dbscan
    outfile = do_dbscan(infile)                          # point cloud file after dbscan
    visualize_pcd.show_pcd(outfile)
