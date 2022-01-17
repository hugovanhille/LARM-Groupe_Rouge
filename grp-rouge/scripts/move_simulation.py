#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

direction = 0
timer = 0

# la fonction move permet de faire avancer le robot ou le faire tourner en cas de présence d'un obstacle sur son chemin
def move(data):
    global direction
    global timer
    move = Twist()

    if direction == 2 :                 #Tourner le robot dans le sens horaire
        move.linear.x = -0.1
        move.angular.z = -0.6
    elif direction == 1 :               #Tourner le robot dans le sens antihoraire
        move.linear.x = -0.1
        move.angular.z = 0.6
    else :                              #Avancer le robot
        move.linear.x = 1
        move.angular.z = 0.0

    pub.publish(move)
    if timer != 0 :
        timer = timer-1

# la fonction callback permet de détecter les obstacles à proximité du robot et de définir la direction à prendre en cas de présence d'un obstacle sur le chemin du robot

def callback(data):
    global direction
    global timer

    liste_obstacles = []                
    min= data.angle_min
    for dist in data.ranges :                  #Boucles permettant de référencer tous les obstacles à proximité du robot
        if 0.05 < dist and dist < 0.6 :
            if (min<=90):
                angle=90-min
            elif (min<=180):
                angle=180-min
            elif (min<=270):
                angle-=180
            else :
                angle-=270
            aPoint= [ 
                    math.cos(angle) * dist,               #Calcul des coordonées de l'obstacle
                    math.sin(angle) * dist
            ]
            liste_obstacles.append(aPoint)          #Ajout de l'obstacle dans la liste
        min+= data.angle_increment
    

    if timer == 0 : 

        direction = 0
        for obstacle in liste_obstacles :                                           #Pour chaque obstacle
            if -0.2 < obstacle[0] and obstacle[0] < 0.2 and abs(obstacle[1]>0.4):            #on regarde s'il est situé sur le chemin de notre robot
                    choice = 0
                    if data.ranges[10] > data.ranges[350]  :
                        direction = 2
                    else :
                        direction = 1
                    timer = 20



pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
rospy.init_node('challenge1', anonymous=True)
rospy.Subscriber("scan", LaserScan, callback)
rospy.Timer(rospy.Duration(0.05), move)

rospy.spin()
