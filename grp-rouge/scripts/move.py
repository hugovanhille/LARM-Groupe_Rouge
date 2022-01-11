import rospy
import tf
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

tfListener= 0
goal= 0

def listen_goal(data):
    global goal 
    goal= data
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def callback2(data):
    local_goal= tfListener.transformPose("/base_footprint", goal)

    rospy.loginfo()

def main():
    global tfListener


    rospy.init_node('move-to', anonymous=True)

    tfListener= tf.TransformListener()
    rospy.Subscriber("goal", PoseStamped, listen_goal)
    rospy.Timer( rospy.Duration(0.1), callback2, oneshot=False )
    
    
    rospy.spin()

if __name__ == '__main__':
    main()