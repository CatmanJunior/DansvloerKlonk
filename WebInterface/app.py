"""
This is the main file for the Flask app. It contains the routes and the main function.
To run the app, run this file with python. 
python app.py
it will run on localhost:5000
"""

import json
import time
from typing import Any, Dict
from flask import Flask, Response, jsonify, render_template, request, stream_with_context
from constants import TOPICS, MIDILIST, BLACK, BROWN, ORANGE, LBLUE, PURPLE, RED, YELLOW, LBROWN, GREY, DBLUE, DGREEN
from sequencer import Sequencer
from sample import Sample
from mqtt_manager import MQTTManager
from threading import Timer
app = Flask(__name__)
# app.debug = True  # Enable debug mode

mqttManager = MQTTManager(topic_list=list(TOPICS.values()))

sampleList = [
    Sample(id=0, name="---",
           midi_values=MIDILIST[0], svg="default.svg", led_color=BLACK, nfc_address="address_0"),
    Sample(id=56, name="poep",
           midi_values=MIDILIST[8], svg="poep.svg", led_color=BROWN, nfc_address="address_56"),
    Sample(id=59, name="kip",
           midi_values=MIDILIST[5], svg="kip.svg", led_color=ORANGE, nfc_address="address_59"),
    Sample(id=51, name="gitaar",
           midi_values=MIDILIST[3], svg="gitaar.svg", led_color=LBLUE, nfc_address="address_51"),
    Sample(id=52, name="bas",
           midi_values=MIDILIST[10], svg="bas.svg", led_color=PURPLE, nfc_address="address_52"),
    Sample(id=53, name="brandweer",
           midi_values=MIDILIST[1], svg="brandweer.svg", led_color=RED, nfc_address="address_53"),
    Sample(id=54, name="sax",
           midi_values=MIDILIST[7], svg="sax.svg", led_color=YELLOW, nfc_address="address_54"),
    Sample(id=55, name="leeuw",
           midi_values=MIDILIST[4], svg="leeuw.svg", led_color=LBROWN, nfc_address="address_55"),
    Sample(id=58, name="robot",
           midi_values=MIDILIST[6], svg="robot.svg", led_color=GREY, nfc_address="address_58"),
    Sample(id=67, name="donder",
           midi_values=MIDILIST[2], svg="donder.svg", led_color=BROWN, nfc_address="address_67"),
    Sample(id=68, name="banaan",
           midi_values=MIDILIST[0], svg="banaan.svg", led_color=YELLOW, nfc_address="address_68"),
    Sample(id=69, name="mic",
           midi_values=MIDILIST[0], svg="mic.svg", led_color=DBLUE, nfc_address="address_69"),
    Sample(id=60, name="eend",
           midi_values=MIDILIST[9], svg="eend.svg", led_color=DGREEN, nfc_address="address_60"),
]


def sequencer_callback(message: str, value: Dict[str, Any]):
    if message == "beat":
        mqttManager.send_message(TOPICS["next_beat"], value)
    elif message == "set_tile_color":
        mqttManager.send_message(TOPICS["set_tile_color"], value)
    elif message == "assign_sample_to_tile":
        mqttManager.send_message(TOPICS["set_tile_color"], value)


def on_message(data: Dict[str, str]):
    """Callback function for MQTTManager. Called when a message is received."""
    if data["topic"] == "tile_nfc":
        sequencer.assign_sample_to_tile(
            int(data["id"]), int(data["sample_id"]))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-message')
def send_message():
    mqttManager.send_message(
        TOPICS["set_tile_color"], {"tile_id": "0", "color": "255255255"})
    mqttManager.send_message(
        TOPICS["tile_nfc"], {"id": "0", "sample_id": "0"})
    return {"Msg": "Message sent"}

#Stream data to the client
#Send everytime the beat changes
@app.route('/stream-data')
def stream_data():
    def generate():
        last_sent_beat = None
        while True:
            if sequencer.current_beat != last_sent_beat:
                data = {"current_beat": sequencer.current_beat, "message_list": mqttManager.message_list[-10:]}
                json_data = json.dumps(data)
                yield f"data:{json_data}\n\n"
                last_sent_beat = sequencer.current_beat
            time.sleep(0.05)  # sleep for a short time to prevent busy-waiting
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/get_update')
def get_update():
    # Generate or fetch the update data
    data = {"current_beat": sequencer.current_beat,
            "message_list": mqttManager.message_list[-10:]}

    return jsonify(data)


if __name__ == '__main__':
    # Create a Sequencer object with 16 tiles and 120 bpm
    sequencer = Sequencer(16, 120, sequencer_callback, sampleList)

    sequencer.update()

    mqttManager.connect("localhost")  # Connect to the MQTT broker
    mqttManager.set_callback(on_message)  # Set the callback function

    app.run(debug=True)
