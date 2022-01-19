#!/usr/bin/python3

import rospy
import numpy as np
import rospy, tf
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped

def dist_bottle(marker1, marker2):
    p1 = np.array([marker1.pose.position.x, marker1.pose.position.y, marker1.pose.position.z])
    p2 = np.array([marker2.pose.position.x, marker2.pose.position.y, marker2.pose.position.z])
    carre = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(carre)
    return dist


def callback(data):

    new_coor = tfListener.transformPose("/pose_robot", data)
    marker.header.frame_id = "odom"
    marker.id = len(marker_array)
    marker.type = marker.CUBE
    marker.action = marker.ADD
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    marker.color.a = 1.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0
    marker.pose.orientation.w = 1.0

    marker.pose.position.x = new_coor.pose.position.x
    marker.pose.position.y = new_coor.pose.position.y
    marker.pose.position.z = new_coor.pose.position.z


    
    if not bool(marker_array):
        marker_array.append(marker)
        pub.publish(marker)


    elif len(marker_array) > 1:
        dist1 = dist_bottle(marker, marker_array[-1])
        
        for i in range(len(marker_array)-1):
            dist2 = dist_bottle(marker, marker_array[i])
            if dist1 > dist_entre_bottle and dist2 > dist__meme_bouteille:
                if marker.id != marker_array[-1].id:
                    marker_array.append(marker)
                    pub.publish(marker)
                else:
                    break
    else:
        dist1 = dist_bottle(marker, marker_array[-1])
        if dist1 > dist_entre_bottle:
            marker_array.append(marker)
            pub.publish(marker)


def main():
    global pub,tfListener,marker_array,dist__meme_bouteille,dist_entre_bottle, marker
    marker = Marker()
    rospy.init_node('marker')
    pub = rospy.Publisher('/bottle', Marker, queue_size=10)
    tfListener = tf.TransformListener()
    marker_array = []
    dist__meme_bouteille = 0.7    
    dist_entre_bottle = 0.40
    rospy.Subscriber("/data_bottle", PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    main()
