#!/usr/bin/env python3
from time import sleep
import rospy
from std_msgs.msg import Float32MultiArray


def print_pos(x,y):
    print("Current caddy position: X: {:0.2f} Y: {:0.2f}".format(x,y))

class caddie:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.dest_x = 0.0
        self.dest_y = 0.0

    def handler(self, msg):
        self.dest_x = msg.data[0]
        self.dest_y = msg.data[1]

        if (self.dest_x - self.x) != 0.0:
            self.reaction()
        else:
            move.data = [self.x,self.y]
            pub.publish(move)

    def reaction(self): 

        while self.x < self.dest_x:
            self.x += 0.1
            move.data = [self.x,self.y]
            print_pos(self.x,self.y)
            pub.publish(move)
            sleep(0.5)
       
        while self.x > self.dest_x:
            self.x -= 0.1
            move.data = [self.x,self.y]
            print_pos(self.x,self.y)
            pub.publish(move)
            sleep(0.5)     

        if self.x == self.dest_x:
            sleep(3)

if __name__ == '__main__':
    server=caddie()
    rospy.init_node('Caddie', anonymous=True)
    pub = rospy.Publisher('pos_caddie',Float32MultiArray, queue_size= 1)
    rospy.Subscriber('destination_caddie', Float32MultiArray, server.handler)
    move = Float32MultiArray()   

    rospy.spin()