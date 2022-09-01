#!/usr/bin/env python
import json
import paho.mqtt.client as mqtt
import rospy
from geometry_msgs.msg import Twist





def turtle_move(cmd):
     
    rospy.init_node('turtlesim', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel = Twist()
    if cmd == "arr up":
        vel.linear.x = 0.2
        print("going up")
    elif cmd == "arr down":
        vel.linear.x =-0.2
        print("going down")
    elif cmd == "arr left":
        vel.linear.y =0.2
        print("going left")
    elif cmd == "arr right":
        vel.linear.y =-0.2
        print("going right")
    elif cmd == "stop":
        vel.linear.x =0
        vel.linear.y =0
        vel.linear.z =0
        print("stop")
       
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
    
    
    turtle_move(cmd["cmd"])
    

    


broker_address = "farlab.infosci.cornell.edu"  # use external broker
client = mqtt.Client("ROS_Teleop_robot")  # create new instance
client.tls_set()  # set tls for the mqtt connection
client.on_connect = on_connect  # attach function callback
client.on_message = on_message  # attach function to callback
client.username_pw_set("testuser", "far1@FAR")

try:
    client.connect(broker_address, 8883)  # connect to broker
except:
    print("connection failed")
    exit(1)  # Should quit or raise flag to quit or retry
print("Subscribing to topic", "teleop")

client.subscribe("teleop")  # subscribe to the topic
client.loop_forever()  # Start loop

