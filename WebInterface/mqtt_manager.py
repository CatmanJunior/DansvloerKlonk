import json
import time
from typing import Any, Dict, List, Literal, LiteralString

import paho.mqtt.client as mqtt

class MQTTManager:
    def __init__(self, broker_address : str = "localhost", topic_list : List[str] = ["sample/set"]):
        self.client = mqtt.Client()
        self.callback = None
        self.message_list = []
        self.topic_list = topic_list
        self.broker_address = broker_address
        
        
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic in self.topic_list:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        self.message_list.append(payload)
        data = dict(json.loads(payload))
        
        if not "topic" in data.keys():
            data["topic"] = msg.topic
        print(f"Received message on [{msg.topic}]: {data}")
        if self.callback:

            self.callback(data)
            
    def set_callback(self, callback):
        self.callback = callback

    def connect(self, broker_address):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, 1883, 60)
        self.client.loop_start()
        
    def send_message(self, topic, message : Dict[str, Any]):
        # send topic time and message
        current_time = time.time()
        formatted_time = time.strftime('%H:%M:%S', time.localtime(current_time))

        message["time"] = formatted_time	
        self.client.publish(topic, json.dumps(message))