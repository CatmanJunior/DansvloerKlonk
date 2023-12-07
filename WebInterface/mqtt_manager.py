import json
from typing import Dict

import paho.mqtt.client as mqtt

class MQTTManager:
    def __init__(self):
        self.client = mqtt.Client()
        self.callback = None
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("sample/set")

    def on_message(self, client, userdata, msg):
        print(f"Received message on {msg.topic}: {msg.payload.decode()}")
        if self.callback:
            data = dict(json.loads(msg.payload.decode()))
           
            self.callback(data)
            

    def set_callback(self, callback):
        self.callback = callback

    def connect(self, broker_address):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, 1883, 60)
        self.client.loop_start()
        
    def send_message(self, topic, message):
        self.client.publish(topic, message)