#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""
import sys
import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def bag_to_jpg(ros_bag,dir,topic):
    """Extract a folder of images from a rosbag.
    """
    data = {
        "bag_file": ros_bag,
        "output_dir": dir,
        "image_topic": topic
    }

    print("Extract images from %s on topic %s into %s" % (data["bag_file"], data["image_topic"], data["output_dir"]))

    bag = rosbag.Bag(data["bag_file"], "r")
    bridge = CvBridge()
    count = 0
    print("Extracting images ...")
    for topic, msg, t in bag.read_messages(topics=[data["image_topic"]]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        cv2.imwrite(os.path.join(data["output_dir"], "frame%04i.png" % count), cv_img)

        count += 1
    print("%i images were extracted" % count)
    bag.close()

    return

if __name__ == '__main__':
    if len(sys.argv) == 1:
        ros_bag = "example_synced.bag"
        topic_pcd = "/os1_cloud_node/points"
        topic_img = "/pylon_camera_node/image_raw"
    elif len(sys.argv) == 2:
        ros_bag = sys.argv[1]
        topic_pcd = "/os1_cloud_node/points"
        topic_img = "/pylon_camera_node/image_raw"
    elif len(sys.argv) == 3:
        ros_bag = sys.argv[1]
        topic_pcd = sys.argv[2]
        topic_img = "/pylon_camera_node/image_raw"
    else:
        ros_bag = sys.argv[1]
        topic_pcd = sys.argv[2]
        topic_img = sys.argv[3]
    bag_to_jpg(ros_bag,topic_pcd,topic_img)
