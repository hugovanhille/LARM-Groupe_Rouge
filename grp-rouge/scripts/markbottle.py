#!/usr/bin/python3

import rospy
import numpy as np
import rospy, tf
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped





SAME_BOTTLE_RADIUS = 0.35         # Distance sous laquelle on considère que c'est la même bouteille qui a été détectée
DIST_MIN_BETWEEN_BOTTLES = 0.3    # Distance minimal entre deux bouteilles différentes

python_marker_array = []          # Liste itérable contenant les markers placés sur la map

# Fonction permettant de calculer la distance entre 2 markers
def compute_dist_between_two_markers(marker1, marker2):
    p1 = np.array([marker1.pose.position.x, marker1.pose.position.y, marker1.pose.position.z])
    p2 = np.array([marker2.pose.position.x, marker2.pose.position.y, marker2.pose.position.z])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist


def callback(data):

    new_coor = tfListener.transformPose("/odom", data)

    # On crée un marker
    marker = Marker()
    marker.header.frame_id = "odom"
    marker.id = len(python_marker_array)
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

    # On lui donne les coordonnées de la bouteille dans la frame "odom"
    marker.pose.position.x = new_coor.pose.position.x
    marker.pose.position.y = new_coor.pose.position.y
    marker.pose.position.z = new_coor.pose.position.z

    
    # Le premier marker est toujours placé
    if len(python_marker_array) == 0:
        python_marker_array.append(marker)
        pub.publish(marker)

    else:
        # On calcule la distance entre le nouveau marker et le dernier placé
        dist1 = compute_dist_between_two_markers(marker, python_marker_array[-1])
        if len(python_marker_array) > 1:
            for i in range(len(python_marker_array)-1):
                # On calcule la distance entre le nouveau marker et ceux qui ont déjà été placés à l'exception du dernier posé
                dist2 = compute_dist_between_two_markers(marker, python_marker_array[i])
                # Si le nouveau marker est loin des autres bouteilles posées et qu'il n'y a pas d'autres bouteilles dans un rayon proche, on pose un nouveau marker
                if dist1 > DIST_MIN_BETWEEN_BOTTLES and dist2 > SAME_BOTTLE_RADIUS:
                    # On vérifie qu'on ne publie pas deux fois le même marker
                    if marker.id != python_marker_array[-1].id:
                        python_marker_array.append(marker)
                        pub.publish(marker)
                    else:
                        break
        
        # Si un seul marker a été placé on en place un nouveau ssi il est assez loin du premier placé
        else:
            if dist1 > DIST_MIN_BETWEEN_BOTTLES:
                python_marker_array.append(marker)
                pub.publish(marker)


def main():
    global pub,tfListener
    rospy.init_node('marker')
    pub = rospy.Publisher('/bottle', Marker, queue_size=10)
    tfListener = tf.TransformListener()
    rospy.Subscriber("/data_bottle", PoseStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    main()
