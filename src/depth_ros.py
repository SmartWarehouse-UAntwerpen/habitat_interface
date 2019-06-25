#!/usr/bin/env python
# note need to run viewer with python2!!!


import rospy
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
import std_msgs.msg
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


pub = rospy.Publisher("ros_img_depth", Image, queue_size=10)
camera_info_pub = rospy.Publisher("camera_info_topic", CameraInfo, queue_size=0)


def callback(data):
    print(rospy.get_name(), "I heard %s" % str(data.data))

    img = np.float32((np.reshape(data.data, (256, 256))))

    h = std_msgs.msg.Header()
    h.stamp = rospy.Time.now()
    image_message = CvBridge().cv2_to_imgmsg(img, encoding="passthrough")
    image_message.header = h
    pub.publish(image_message)

    camera_info_msg = CameraInfo()
    camera_info_msg.header = h
    width, height = 256, 256
    fx, fy = 256 / 2, 256 / 2
    cx, cy = 128, 128
    camera_info_msg.width = width
    camera_info_msg.height = height
    camera_info_msg.distortion_model = "plumb_bob"
    camera_info_msg.K = np.float32([fx, 0, cx, 0, fy, cy, 0, 0, 1])

    camera_info_msg.D = np.float32([0, 0, 0, 0, 0])

    camera_info_msg.P = [fx, 0, cx, 0, 0, fy, cy, 0, 0, 0, 1, 0]

    camera_info_pub.publish(camera_info_msg)


def listener():
    rospy.init_node("gray2ros_depth")
    rospy.Subscriber("depth", numpy_msg(Floats), callback)
    rospy.spin()


if __name__ == "__main__":
    listener()
