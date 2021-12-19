#!/usr/bin/python3
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

obstacles= []

# Publish velocity commandes:
def move_front(data):
    cmd= Twist()
    cmd.linear.x= 2
    commandPublisher.publish(cmd)


def move_command_angular(data):
    cmd= Twist()
    cmd.angular.z= 1
    #cmd.linear.x= -0.2
    commandPublisher.publish(cmd) 

# Publish velocity commandes:
#Va recup les obstacle dans une liste global qu'on v apouvoir mettre à jour
def interpret_scan(data):
    global obstacles
    rospy.loginfo('I get scans')
    obstacles= []
    angle= data.angle_min #angle minimum 
    
    #Comment est cosntruit obstacle ?
    for aDistance in data.ranges : # on parcourt le parametre range de data cad le tableau immense de point
        
        if 0.1 < aDistance and aDistance < 5.0 : # Si la distance est trop petite
            aPoint= [ 
                math.cos(angle) * aDistance, #on obtient x
                math.sin( angle ) * aDistance #on obtient y
            ]
            obstacles.append( aPoint ) #on ajoute
        angle+= data.angle_increment #on passe à langle suivant
    rospy.loginfo( str(
        [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    ) + " ..." )

def faire_evoluer_robot(data):
    t=0
    for a in obstacles :
        if -taille_x < a[0] < taille_x :		#S'il y a quelquechose dans l'enveloppe de notre turtlebot
            if -taille_y < a[1] < taille_y  and t==0:
                t=1
                
    if t == 0:
        move_front(data)
    else:
        move_command_angular(data)
        


#taille
taille_x = 0.2
taille_y = 0.1

rospy.init_node('move', anonymous=True)

# connect to the topic:
rospy.Subscriber('scan', LaserScan, interpret_scan)

# call the aire_evoluer_robot at a regular frequency:
rospy.Timer( rospy.Duration(0.4), faire_evoluer_robot, oneshot=False )
#spin() enter the program in a infinite loop
print("Lancement de challenge1.py")
rospy.spin()
print("Fin")
