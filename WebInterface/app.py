"""
This is the main file for the Flask app. It contains the routes and the main function.
To run the app, run this file with python. 
python app.py
it will run on localhost:5000
"""
from flask import Flask, render_template
from livereload import Server
from livereload.watcher import Watcher

app = Flask(__name__)
app.debug = True  # Enable debug mode

class CustomWatcher(Watcher):
    def is_glob_changed(self, path):
       return True
    
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.watcher = CustomWatcher()  # Use the custom watcher
    server.serve(port=5000, liveport=35729)  # Specify the liveport for browser synchronization
