#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

direction = 0
timer = 0

# move(data) is the function that will publish the directions to move the robot
# depending on the 'direction' variable modified in the other functions 
def move(data):
    global direction
    global timer
    move_cmd = Twist()
    if direction == 2 :
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = -0.6
    elif direction == 1 :
        move_cmd.linear.x = 0.0
        move_cmd.angular.z = 0.6
    else :
        move_cmd.linear.x = 0.5
        move_cmd.angular.z = 0.0
    pub.publish(move_cmd)
    if timer != 0 :
        timer -= 1

# choix(liste_obstacles) is called when a collision is detected and will 
# analyse the environnement to choose in with direction it is better to
# turn to avoid the collision

# detect_collision(liste_obstacles) will choiceide if there is a collision danger 
# with one of the liste_obstacles detected and will then execute choix

# callback(data) uses the data provided by the topic from the 
# laser to create a list of points that are liste_obstacles seen by the laser

def callback(data):
    global direction
    global timer

    liste_obstacles = []
    min= data.angle_min
    for dist in data.ranges :
        if 0.2 < dist and dist < 0.6 :
            aPoint= [ 
                math.cos(min) * dist, 
                math.sin(min) * dist
            ]
            liste_obstacles.append(aPoint)
        min+= data.angle_increment
    

    if timer == 0 : 

        direction = 0
        for obstacle in liste_obstacles : 
            if 0.2 < obstacle[0] and obstacle[0] < 0.6 and abs(obstacle[1]>0.3):
                    choice = 0
                    for obstacle in liste_obstacles :
                        if 0.2 < obstacle[0] and obstacle[0] < 0.5 and abs(obstacle[1]>0.2):
                            choice += obstacle[1]
                    if choice >= 0 :
                        direction = 2
                    else :
                        direction = 1
                    timer = 20


# main_prog() contains the main structure of the program : 
# callbacks from laser scans and a regular publishing to move the robot

pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
rospy.init_node('challenge1', anonymous=True)
rospy.Subscriber("scan", LaserScan, callback)
rospy.Timer(rospy.Duration(0.1), move)

rospy.spin()

