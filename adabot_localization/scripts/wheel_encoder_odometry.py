#!/usr/bin/env python

"""
This node is responsible for turning join state information
into wheel-encoder based odometry.

For detecting slippage, we'll need to do the following:

1. Subscribe to the /adabot/joint_states topic.
2. Convert wheel angular velocities into linear velocity
    a. This requies us to know the radius of the wheels (parameter server?)
    b. We'll also need to take into acount the weg extension length
3. Subscribe to the

> rosmsg show sensor_msgs/JointState
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
string[] name
float64[] position
float64[] velocity
float64[] effort
"""

import rospy
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


forward_speed = 0
wheel_radius = None


def joint_state_callback(data):
    """ Calculate the velocity of the robot based on wheel joint data """

    # wheel_names = [data.name[i] for i in wheel_indices]
    # wheel_positions = [data.position[i] for i in wheel_indices]
    # wheel_efforts = [data.effort[i] for i in wheel_indices]

    global forward_speed

    wheel_indices = [i for i, s in enumerate(data.name) if '_wheel_joint' in s]
    wheel_velocities = [data.velocity[i] for i in wheel_indices]

    if wheel_radius != None:
        forward_speed = sum(wheel_velocities) / len(wheel_velocities) * wheel_radius
    # print data.twist[data.name.index('adabot::base_link')]


def publish_odometry():

    # AJC: make this configurable
    rate = rospy.Rate(30)
    odom_publisher = rospy.Publisher('adabot/odometry', Odometry, queue_size=10)
    odom_broadcaster = TransformBroadcaster()

    while not rospy.is_shutdown():

        current_time = rospy.get_rostime()

        # Publish the transform over tf
        odom_transform = TransformStamped()
        odom_transform.header.stamp = current_time
        odom_transform.header.frame_id = 'odom'
        odom_transform.child_frame_id = 'base_link'
        odom_transform.transform.rotation.w = 1
        odom_broadcaster.sendTransform(odom_transform)

        # Publish the odometry message over ROS
        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        # odom.pose.pose = 0
        odom.twist.twist.linear.x = forward_speed
        odom_publisher.publish(odom)

        rate.sleep()


if __name__ == '__main__':
    # Initialize this node
    rospy.init_node('adabot_odometry')

    # Listen to the joint states published by ros_control
    rospy.Subscriber('adabot/joint_states', JointState, joint_state_callback)

    # Get the wheel radius from the parameter server
    wheel_radius = rospy.get_param('wh_radius')

    # Go into the publish loop
    try:
        publish_odometry()
    except rospy.ROSInterruptException:
        pass
