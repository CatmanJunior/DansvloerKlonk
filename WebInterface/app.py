"""
This is the main file for the Flask app. It contains the routes and the main function.
To run the app, run this file with python. 
python app.py
it will run on localhost:5000
"""
from os import curdir
import re
import time
from turtle import st
from typing import Dict
from flask import Flask, Response, jsonify, render_template, request, stream_with_context
from livereload import Server
from livereload.watcher import Watcher
from sequencer import Sequencer

from mqtt_manager import MQTTManager
from threading import Timer
app = Flask(__name__)
app.debug = True  # Enable debug mode

mqqManager = MQTTManager()  # Create an MQTTManager object

sequencer = Sequencer(16, 120)  # Create a Sequencer object with 16 tiles and 120 bpm

message_list = []

def on_message(data: Dict[str, str]):
    """Callback function for MQTTManager. Called when a message is received."""
    print("Received message: ", data)
    message_list.append(data)
    # if data["id"] == "all":
    #     for i in range(16):
    #         sequencer.assign_sample_to_tile(i, data["sample_id"])
    # else:
    #     sequencer.assign_sample_to_tile(int(data["id"]), data["sample_id"])

class CustomWatcher(Watcher):
    def is_glob_changed(self, path):
        return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-message')
def send_message():

    #send topic time and message
    mqqManager.send_message("sample/set", '{"time": 0, "topic": "sample/set", "body": "test"}')
    return "Message sent"


@app.route('/stream_updates')
def streamed_response():

    def generate():
        while True:
            
            yield f"data: {sequencer.current_beat}\n\n"
            time.sleep(1)
            
    return Response(stream_with_context(generate()), mimetype='text/json')

@app.route('/get_update')
def get_update():
    # Generate or fetch the update data
    data = {"current_beat": sequencer.current_beat,"message_list": message_list[-10:]}
    mqqManager.send_message("sample/set", '{"time": 0, "topic": "sample/set", "body": "test"}')

    return jsonify(data)



if __name__ == '__main__':
    sequencer.update()

    mqqManager.connect("localhost")  # Connect to the MQTT broker
    mqqManager.set_callback(on_message)  # Set the callback function

    server = Server(app.wsgi_app)
    server.watcher = CustomWatcher()  # Use the custom watcher
    # Specify the liveport for browser synchronization
    server.serve(port=5000, liveport=35729)
