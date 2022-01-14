#!/usr/bin/python3
import rospy
import cv2
import numpy as np
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import math

bridge = CvBridge()
 

def interpret_image(data):
    temp_frame=data
    global bridge,color,lo,hi,color_info,disArr, timeStamp
    timeStamp= temp_frame.header.stamp
    frame = bridge.imgmsg_to_cv2(temp_frame, desired_encoding='passthrough')
    cv2.namedWindow('Camera')
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Camera',frame )
    cv2.waitKey(40)
    cmd=PoseStamped()

    image=cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    
    image=cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=1)
    mask=cv2.dilate(mask, None, iterations=1)
    image2=cv2.bitwise_and(frame, frame, mask= mask)
        # Affichage des composantes HSV sous la souris sur l'image
    image=cv2.blur(image, (7, 7))
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=6)
    mask=cv2.dilate(mask, None, iterations=6)
                

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
    if len(elements) > 0:
        c=max(elements, key=cv2.contourArea)
        rec=cv2.boundingRect(c)
        ((x, y), rayon)=cv2.minEnclosingCircle(c)
        profondeur=disArr[int(y)][int(x)]
        coorx=int(rec[0]+(rec[2])/2)
        coorFin=Coor(coorx,profondeur)
        if 20<rayon and 4000>profondeur>10:
            cmd=createPoseStampedPub(int(coorFin[0]),int(coorFin[1]))
            if cmd.pose.position.x<2 and cmd.pose.position.y<1:
                pub.publish(cmd)
                cv2.circle(image2, (int(x), int(y)), int(rayon), color_info, 2)
                cv2.circle(frame, (int(x), int(y)), 5, color_info, 10)
                cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_info, 2)
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)
                    
 
cv2.destroyAllWindows()

def createPoseStampedPub(x,y):
    cmd=PoseStamped()
    cmd.header.stamp=timeStamp
    cmd.header.frame_id='camera_link'
    cmd.pose.position.x=x/1000
    cmd.pose.position.x+=0.15
    cmd.pose.position.y=-y/1000
    if cmd.pose.position.y<0:
        cmd.pose.position.y-=0.1
    else :
        cmd.pose.position.y+=0.1
    cmd.pose.position.z=0
    cmd.pose.orientation.x=0
    cmd.pose.orientation.y=0
    cmd.pose.orientation.z=0
    cmd.pose.orientation.w=1
    return cmd


def Coor(x,pro):
    
    angle=43.55*(x-640)/640
    angle=angle*math.pi/180 # passage en radians
    return [math.cos(angle) * pro, math.sin( angle ) * pro-35] 

def distance(data):
    global disArr
    disArr=np.array(bridge.imgmsg_to_cv2(data,desired_encoding="passthrough"))

def detection():
    global lo,hi,pub,color_info
    rospy.init_node('objet', anonymous=True)
    pub = rospy.Publisher(
        'can',   
        PoseStamped, queue_size=10
    )
    rospy.loginfo(rospy.get_caller_id() + 'I heard ')

    lo=np.array([95, 240, 230])
    hi=np.array([110, 255,255])
    rate=rospy.Rate(10)
    color_info=(0, 0, 255)
    rospy.Subscriber('camera/color/image_raw', Image, interpret_image)
    rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image , distance)

    rospy.spin()

if __name__ == '__main__':
    detection()
