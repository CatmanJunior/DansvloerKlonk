from flask import Flask, Response, stream_with_context
import time

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route('/stream')
def stream():
    def generate():
        num = 0
        while True:
            yield f"data: {num}\n\n"
            num += 1
            time.sleep(1)

    return Response(stream_with_context(generate()), content_type='text/event-stream')



if __name__ == '__main__':
    app.run(debug=True)
