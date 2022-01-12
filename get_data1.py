import subprocess
import sys
import os
import os.path


def print_info(rosbag):
    cmd = ['time', 'rosbag', 'info', rosbag]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    print('Output: ' + o.decode('ascii'))


def to_pcd(rosbag, topic):
    cmd = ['rosrun', 'pcl_ros', 'bag_to_pcd', rosbag, topic, './pointclouds']
    # subprocess.run(cmd, shell=True, check=True)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("PCD files are in ./pointclouds folder")


def change_images_dir(path):
    command = "mv ~/.ros/frame*.jpg " + path
    os.system(command)


def move_images():
    cwd = os.path.abspath(os.getcwd())
    path = os.path.join(cwd, "images")
    if os.path.exists("images"):
        change_images_dir(path)
    else:
        os.mkdir(path)
        change_images_dir(path)
    print("Images saved in ./images folder")


def get_images(rosbag, topic_img):
    cwd = os.path.abspath(os.getcwd())
    path = os.path.join(cwd, "export_img.launch ")
    bagfile = "bagfile:=" + os.path.join(cwd, rosbag)
    topic = " topic:=" + topic_img
    command = "roslaunch " + path + bagfile + topic
    print(command)
    os.system(command)
    move_images()


def get_data_from_rosbag(rosbag, topic_pcd="/os1_cloud_node/points", topic_img="/pylon_camera_node/image_raw"):
    print_info(rosbag)
    to_pcd(rosbag, topic_pcd)
    get_images(rosbag, topic_img)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        rosbag = "example_synced.bag"
        topic_pcd = "/os1_cloud_node/points"
        topic_img = "/pylon_camera_node/image_raw"
    elif len(sys.argv) == 2:
        rosbag = sys.argv[1]
        topic_pcd = "/os1_cloud_node/points"
        topic_img = "/pylon_camera_node/image_raw"
    elif len(sys.argv) == 3:
        rosbag = sys.argv[1]
        topic_pcd = sys.argv[2]
        topic_img = "/pylon_camera_node/image_raw"
    else:
        rosbag = sys.argv[1]
        topic_pcd = sys.argv[2]
        topic_img = sys.argv[3]

    get_data(rosbag, topic_pcd, topic_img)



