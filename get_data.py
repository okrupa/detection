import subprocess
import sys
import os
import os.path
from delete_files import delete_files_in_directory


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


def get_images(rosbag, topic_img):
	cwd = os.path.abspath(os.getcwd())
	path_img = os.path.join(cwd, "images")

	folder = "images"
	if os.path.exists(folder):
		delete_files_in_directory(folder)
	else:
		os.mkdir(folder)

	bagfile = os.path.join(cwd, rosbag)
	topic = topic_img
	s = " "
	command = "python bag_to_images.py " + bagfile + s + path_img + s + topic
	print(command)
	os.system(command)

	print("Images saved in ./images folder")


def get_data_from_rosbag(rosbag, topic_pcd = "/os1_cloud_node/points",topic_img = "/pylon_camera_node/image_raw"):
	print_info(rosbag)
	folder = "pointclouds"
	if os.path.exists(folder):
		delete_files_in_directory(folder)
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
	
	get_data_from_rosbag(rosbag,topic_pcd, topic_img)

	
	
