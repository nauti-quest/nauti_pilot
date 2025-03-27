#!/usr/bin/python3
import rospy

from nauti_pilot.msg import Command

from mavros_msgs.msg import OverrideRCIn as rc
from mavros_msgs.srv import StreamRate
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State
import mavros
import mavros.command 

pubRC = None,
rc_msg = None
neutral_speed = 1500
new_command = False

def convert_command(data):
    #This takes the float value from -1.0 to 1.0 and converts it to be between 1100 and 1900
    if(data >0.6): # duty cycle limited to 60%
        return int((0.6 * 400) + neutral_speed)
    else:
	    return int((data * 400) + neutral_speed)

def command_callback(data):
    global pubRC, rc_msg, new_command
    new_command = True
    rc_msg = rc()
    rc_msg.channels[0] = convert_command(data.pitch)
    rc_msg.channels[1] = neutral_speed
    rc_msg.channels[2] = convert_command(data.heave)
    rc_msg.channels[3] = convert_command(data.yaw)
    rc_msg.channels[4] = convert_command(data.throttle*-1)

def set_stream_rate():
    stream_rate = rospy.ServiceProxy('mavros/set_stream_rate', StreamRate)
    stream_rate(0, 10, 1)

def set_manual_mode():
    set_mode = rospy.ServiceProxy('mavros/set_mode', SetMode)
    rospy.wait_for_service('mavros/set_mode')
    set_mode(0, 'MANUAL')

def set_stabilized_mode():
    set_mode = rospy.ServiceProxy('mavros/set_mode', SetMode)
    rospy.wait_for_service('mavros/set_mode')
    set_mode(0, 'STABILIZE')

    
def arm():
    mavros.set_namespace()
    mavros.command.arming(True)

def init_pixhawk():
    set_stream_rate()
    set_manual_mode()
    # set_stabilized_mode()
    arm()

def pilot():
    global pubRC, rc_msg, new_command

    rospy.init_node('pilot', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    pubRC = rospy.Publisher('mavros/rc/override', rc, queue_size=10)
    rospy.Subscriber("loco/command", Command, command_callback)

    init_pixhawk()

    while not rospy.is_shutdown():
        if new_command:
            pubRC.publish(rc_msg)
            new_command = False
            rospy.loginfo('Publishing non-neutral Command')
        else:
            rc_msg = rc()
            rc_msg.channels[0] = neutral_speed
            rc_msg.channels[1] = neutral_speed
            rc_msg.channels[2] = neutral_speed
            rc_msg.channels[3] = neutral_speed
            rc_msg.channels[4] = neutral_speed
            pubRC.publish(rc_msg)
            
        rate.sleep()

    

if __name__ == '__main__':
    try:
        pilot()
    except rospy.ROSInterruptException:
        pass