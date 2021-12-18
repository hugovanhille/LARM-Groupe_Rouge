#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
# Initialize ROS::node
rospy.init_node('move', anonymous=True)

#commandPublisher = rospy.Publisher(
 #   '/cmd_vel_mux/input/navi',
  #  Twist, queue_size=10
#)


cmd= Twist()
def callback(msg):
	if msg.ranges[0]>0.8:
		cmd.linear.x=0.1
		cmd.angular.z=0.0
	elif msg.ranges[0]<0.4:
		if msg.ranges[90]>msg.ranges[270]:
			cmd.linear.x=0.01
			cmd.angular.z=0.5
		else:
			cmd.linear.x=0.01
			cmd.angular.z=-0.5
	pub.publish(cmd)
#rospy.Timer( rospy.Duration(0.1),callback,oneshot=False)
sub= rospy.Subscriber('/scan',LaserScan,callback)
pub=rospy.Publisher('/cmd_vel_mux/input/navi',Twist,queue_size=10)

# Publish velocity commandes:
#def move_command(data):
 #   # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
   # cmd= Twist()
  #  cmd.linear.x= 0.1
    #commandPublisher.publish(cmd)

# call the move_command at a regular frequency:
#rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()

