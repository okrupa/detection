import subprocess
import sys

def print_info(rosbag):
	cmd = ['time', 'rosbag', 'info', rosbag]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	o, e = proc.communicate()
	print('Output: ' + o.decode('ascii'))

def to_pcd(rosbag):
	cmd = ['rosrun', 'pcl_ros', 'bag_to_pcd', rosbag, '/os1_cloud_node/points', './pointclouds']
	# subprocess.run(cmd, shell=True, check=True)
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



if __name__ == "__main__":
	if len(sys.argv)>=2:
		rosbag = sys.argv[1]
	else:
		rosbag = "example_synced.bag"
	print_info(rosbag)
	to_pcd(rosbag)
	print("PCD files are in ./pointclouds folder")
	
