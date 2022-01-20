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


def to_pcd(rosbag, topic, path):
	cmd = ['rosrun', 'pcl_ros', 'bag_to_pcd', rosbag, topic, path]
	# subprocess.run(cmd, shell=True, check=True)
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print("PCD files are in ./pointclouds folder")


def get_images(rosbag, topic_img, path_img, cwd):

	if os.path.exists(path_img):
		delete_files_in_directory(path_img)
	else:
		os.mkdir(path_img)

	bagfile = os.path.join(cwd, rosbag)
	topic = topic_img
	s = " "
	command = "python bag_to_images.py " + bagfile + s + path_img + s + topic
	print(command)
	os.system(command)

	print("Images saved in ./images folder")


def get_data_from_rosbag(rosbag, folder_to_save, topic_pcd = "/os1_cloud_node/points",topic_img = "/pylon_camera_node/image_raw"):
	print_info(rosbag)
	path = folder_to_save+"/pointclouds"
	if os.path.exists(path):
		delete_files_in_directory(path)
	to_pcd(rosbag, topic_pcd, path)
	path_imgs = folder_to_save+"/images"
	get_images(rosbag, topic_img, path_imgs, folder_to_save)
	
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


	
	
