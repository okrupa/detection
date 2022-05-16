import subprocess
import os
import os.path
from functions.delete_files import delete_files_in_directory
from functions.bag_to_images import bag_to_jpg


def print_info(rosbag):
	cmd = ['time', 'rosbag', 'info', rosbag]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = proc.communicate()
	print('Output: ' + o.decode('ascii'))


def to_pcd(rosbag, topic, path):
	print('Extracting pcd files...')
	cmd = ['rosrun', 'pcl_ros', 'bag_to_pcd', rosbag, topic, path]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = proc.communicate()
	print("PCD files are in ./pointclouds folder")


def get_images(rosbag, topic_img, path_img, cwd):
	if os.path.exists(path_img):
		delete_files_in_directory(path_img)
	else:
		os.mkdir(path_img)

	bagfile = os.path.join(cwd, rosbag)
	topic = topic_img
	s = " "
	bag_to_jpg(bagfile, path_img, topic)
	# command = "python functbag_to_images.py " + bagfile + s + path_img + s + topic
	# os.system(command)

	print("Images saved in ./images folder")


def get_data_from_rosbag(rosbag, folder_to_save, topic_pcd = "/os1_cloud_node/points",topic_img = "/pylon_camera_node/image_raw"):
	print_info(rosbag)
	path = folder_to_save+"/pointclouds"
	if os.path.exists(path):
		delete_files_in_directory(path)
	to_pcd(rosbag, topic_pcd, path)
	path_imgs = folder_to_save+"/images"
	get_images(rosbag, topic_img, path_imgs, folder_to_save)



	
	
