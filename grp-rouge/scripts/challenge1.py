#!/usr/bin/python3
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time
print("Normalement j'apparait en premier et à chaque spin")
commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

obstacles= []

# Publish velocity commandes:
#Permet de faire bouger le robot en ligne droite de 0.1
def move_command_linear(data):
    print("move_command_linear(data)")
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    cmd.linear.x= 0.1
    commandPublisher.publish(cmd) #ma meilleure amrospy.spin()

def move_command_angular(data):
    print("move_command_angular(data)")
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    cmd.angular.z= 0.4
    commandPublisher.publish(cmd) #ma meilleure amie

# Publish velocity commandes:
#Va recup les obstacle dans une liste global qu'on v apouvoir mettre à jour
def interpret_scan(data):
    print("Je fait le tableau")
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
    print("Je suis bloquée dans faire_evoluer robot")
    for a in obstacles :
        if -enveloppe_x < a[0] < enveloppe_x :
            if -enveloppe_y < a[1] < enveloppe_y  and t==0:
                t=1
                print("Aie un truc dans l'enveloppe")
    if t == 0:
        move_command_linear(data)
        print("J'avance'")
    else:
        print("Je tourne")
        move_command_angular(data)
        


#enveloppe
enveloppe_x = 0.2
enveloppe_y = 0.1

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

# connect to the topic:
print("interpret_scan")
rospy.Subscriber('scan', LaserScan, interpret_scan)

# call the aire_evoluer_robot at a regular frequency:
print("faire_evoluer_robot")
rospy.Timer( rospy.Duration(0.1), faire_evoluer_robot, oneshot=False )
print("Normalement j'apparait")
#spin() enter the program in a infinite loop
print("Start challenge1.py")
rospy.spin()
print("C'est fini le spin est fini")
