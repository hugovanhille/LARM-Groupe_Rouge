#!/usr/bin/python3

##Importation 

from turtle import color
import rospy
import cv2
import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
import math
import tf

def data_interpreter(data):

    # Lancement de Yolo
    net = cv2.dnn.readNet("/home/hugo/catkin_ws/src/LARM-Groupe_Rouge/grp-rouge/vision/yolov3_training_last.weights", "/home/hugo/catkin_ws/src/LARM-Groupe_Rouge/grp-rouge/vision/yolov3_testing.cfg")
    # Création de la classe bottle et récupération du temps pour le PoseStamped
    classes = ["Bottle"]
    global time
    time=rospy.Time.now()
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    temp_frame=data
    global bridge,color,distance
   
    frame = bridge.imgmsg_to_cv2(temp_frame, desired_encoding='passthrough')
    stamped=PoseStamped()

    # Detection d'objet
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    height,width=frame.shape
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for main in out:
            scores = main[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.9:  # Indice de confidence de la détection d'une bouteille (de 0 à 1)
                # Object detecté
                print(class_id)
                center_x = int(main[0] * width)    #Calcul du centre de la bouteille
                center_y = int(main[1] * height)
                print("le centre est"+ str(center_x)+"," +str(center_y))
                w = int(main[2] * width)
                print("w"+str(w))
                h = int(main[3] * height)
                print("h"+str(h))
                # Rectangle coordinates
                x = int(center_x - w / 2)    # Calcul du centre du rectangle dessiné autour de la bouteille
                y = int(center_y - h / 2)
                str("x"+str(x))
                str("y"+str(y))
               # boxes.append([x, y, w, h])
               # confidences.append(float(confidence))
               # class_ids.append(class_id)
                profondeur=distance[int(y)][int(x)]
                coorx=center_x
                coorFin=calcul_coord(coorx,profondeur)   # Coordonnées de la bouteille par rapport au robot
                stamped=PoseStamped_create(int(coorFin[0]),int(coorFin[1]),time)  #Initialisation et publication du PoseStamped 
                pub.publish(stamped)
    


def PoseStamped_create(x,y,time): #creation du PoseStamped et initialisation
    stamped=PoseStamped()
    stamped.header.stamp= time 
    stamped.header.frame_id='camera_link'
    stamped.pose.position.x=x/1000
    stamped.pose.position.x+=0.15
    stamped.pose.position.y=-y/1000
    if stamped.pose.position.y<0:
        stamped.pose.position.y-=0.1
    else :
        stamped.pose.position.y+=0.1
    stamped.pose.position.z=0
    stamped.pose.orientation.x=0
    stamped.pose.orientation.y=0
    stamped.pose.orientation.z=0
    stamped.pose.orientation.w=1
    return stamped



def calcul_dist(data):   #calcul de la distance entre le robot et la bouteille basé sur la frame
    global distance
    distance=np.array(bridge.imgmsg_to_cv2(data,desired_encoding="passthrough"))


def calcul_coord(x,pro):   #calcul des coordonnées de la bouteille
    angle=43.55*(x-640)/640
    angle=angle*math.pi/180 # passage en radians
    return [math.cos(angle) * pro, math.sin( angle ) * pro-35] 


def main():   # initialisation des variables et définition des Subscriber et publisher
    global pub,bridge,pose_init
    pose_init=[]
    bridge = CvBridge()
    rospy.init_node('camera', anonymous=True)
    pub = rospy.Publisher('/data_bottle',PoseStamped, queue_size=10)
    rospy.loginfo(rospy.get_caller_id() + 'I heard ')
    rospy.Subscriber('/camera/color/image_raw', Image, data_interpreter)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image , calcul_dist)
    rospy.spin()
    cv2.destroyAllWindows()

if __name__ == '__main__': #Boucle toute les 1s sur la fonction main
    rospy.Timer(rospy.Duration(1),main(),oneshot=False)
