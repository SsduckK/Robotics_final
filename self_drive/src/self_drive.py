#!/home/pi/.pyenv/versions/rospy3/bin/python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        turtle_vel = Twist()

        forward = (average(scan.ranges[0:18])+average(scan.ranges[342:359]))/2
        semi_left = average(scan.ranges[19:54])
        left = average(scan.ranges[55:90])
        semi_right = average(scan.ranges[307:342])
        right = average(scan.ranges[270:306])

        print("forward", forward, "\nsemi right", semi_right, "\nright", right, "\nsemi left", semi_left, "\nleft", left, "\n")

        if forward > 0.4:
            turtle_vel.linear.x = 0.2
            turtle_vel.angular.z = 0
            if right < 0.2:
                turtle_vel.angular.z = 1.4
            elif left < 0.2:
                turtle_vel.angular.z = -1.4
        elif forward < 0.4:
            if semi_right > semi_left:
                turtle_vel.angular.z = -1.4
            elif semi_left > semi_right:
                turtle_vel.angular.z = 1.4
            elif right < 0.25:
                turtle_vel.angular.z = 1.6
            elif left < 0.25:
                turtle_vel.angular.z = -1.6

        self.publisher.publish(turtle_vel)


def average(some_list):
    return sum(some_list) / len(some_list)


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=5)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()


if __name__ == "__main__":
    main()