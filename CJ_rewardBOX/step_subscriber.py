import paho.mqtt.client as mqtt
import sys

file = open("IP.txt", 'r')
IP = file.read()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("StepCount")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    step = int(msg.payload)
    #print (step)
    file = open('STEP_output.txt','w')
    step_str = str(step)
    file.write(step_str)
    file.close()
    
def main():    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(IP, 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.


    client.loop_forever()

