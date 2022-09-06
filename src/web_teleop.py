#!/usr/bin/env python
import json
import paho.mqtt.client as mqtt
import rospy
from geometry_msgs.msg import Twist
import socket
 






def turtle_move(x,y):
     
    rospy.init_node('turtlesim', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel = Twist()
    if x == "stop":
        vel.linear.x =0
        vel.linear.y =0
        vel.linear.z =0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = 0
        print("stop")
    else:
        vel.linear.x = y
        vel.angular.z = x
       
    pub.publish(vel)
    rate.sleep()



# onConnect event
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


# new message event
def on_message(client, userdata, message):
    
    print("message received ", str(message.payload.decode("utf-8")))  # print incoming message
    cmd = json.loads(str(message.payload.decode("utf-8")))  # decode JSON message
    
    
    turtle_move(cmd["x"], cmd["y"])
    

    

IP = socket.gethostbyname(socket.gethostname())
broker_address = "farlab.infosci.cornell.edu"  # use external broker
client = mqtt.Client("ROS_Teleop_robot_"+IP)  # create new instance
client.tls_set()  # set tls for the mqtt connection
client.on_connect = on_connect  # attach function callback
client.on_message = on_message  # attach function to callback
client.username_pw_set("testuser", "far1@FAR")

try:
    client.connect(broker_address, 8883)  # connect to broker
except:
    print("connection failed")
    exit(1)  # Should quit or raise flag to quit or retry
print("Subscribing to topic", "teleop_"+IP)

client.subscribe("teleop_"+IP)  # subscribe to the topic
client.loop_forever()  # Start loop
