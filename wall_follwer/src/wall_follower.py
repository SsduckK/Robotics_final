#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class WallFollower:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        turtle_vel = Twist()
        forward = scan.ranges[0]
        left = average(scan.ranges[225:315])
        left_forward = average(scan.ranges[270:315])
        left_behind = average(scan.ragnes[225:270])

        if left >= 0.18 and left <= 0.22:
            turtle_vel.linear.x = 0.15
            turtle_vel.angular.z = 0.0

        elif left > 0.22 and left < 0.5:
            if left_forward > left_behind:
                turtle_vel.angular.z = -(math.pi/2)
                turtle_vel.linear.x = 0.14
            elif left_forward == left_behind:
                turtle_vel.linear.x = 0.15
            else:
                turtle_vel.angular.z = (math.pi/9)
                turtle_vel.linear.x = 0.08

        elif left < 1.8:
            if left_forward > left_behind:
                turtle_vel.angular.z = -(math.pi/9)
                turtle_vel.linear.x = 0.08
            elif left_forward == left_behind:
                turtle_vel.linear.x = 0.15
            else:
                turtle_vel.linear.x = 0.14
                turtle_vel.angular.z = (math.pi/6)
        else:
            turtle_vel.linear.x = 0.15
            turtle_vel.angular.z = 0.0
            if forward[0] <= 0.2:
                turtle_vel.linear.x = 0.0
                turtle_vel.angular.z = (math.pi/2)
            else:
                turtle_vel.linear.x = 0.15
        #self.publisher.publish(turtle_vel)


def average(some_list):
    return sum(some_list)/len(some_list)


def main():
    rospy.init_node('Wall_Follower')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = WallFollower(publisher)
    subscriber = rospy.Subscriber('scan', Laserscan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()