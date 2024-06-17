from operator import call
from constants import *
import paho.mqtt.client as mqtt
# MQTT-------
# The callback for when the client receives a
# CONNACK response from the server.
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # type: ignore
msgCallback = None


def connectToMqtt(msg_Callback=None, exitOnFail=False):
    # client = mqtt.Client(configer['MQTT']['clientName'])
    client.on_connect = on_connect
    client.on_message = on_message

    global msgCallback
    msgCallback = msg_Callback

    if CONNECT_TO_BROKER:
        try:
            client.connect(host=BROKER_IP)
            print("Connected to Broker")
            client.loop_start()
        except Exception as e:
            print("ERROR: Can't connect to MQTT BROKER: " + str(e))
            if exitOnFail:
                exit(1)

def on_connect(client, userdata, flags, rc, prop):
    print("Connected with result code " + str(rc))
    for tile in range(TOTAL_TILES):
        # Subscribe to the tile topics (t0-t15)
        client.subscribe("t" + str(tile))

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    payload = str(msg.payload)[3:-1]
    # Subtopic -> messages are build as a15. a = NFC. s = Sensor.
    subTop = str(msg.payload)[2]
    # if subtopic is s return
    if subTop == "s":
        return
    if DEBUG:
        print("New Message -> Topic: " + msg.topic +
              " | Subtopic: " + subTop + " | Payload: " + payload)
    if msgCallback is not None:
        msgCallback(msg.topic, subTop, payload)

def SendTileColor(tile, color=None):
    if color is None:
        client.publish("led" + str(tile.id), tile.color + "1")
    else:
        client.publish("led" + str(tile.id), color + "1")
    # if DEBUG:
    #     print("message sent to led" + str(tile.id) + " with color " + tile.color)

def Stop():
    client.loop_stop()
    client.disconnect()
    print("MQTT Client Stopped")