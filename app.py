import logging
import time
from flask import Flask, render_template, request, Response

app = Flask(__name__)


data  = []

@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/submitted", methods=["POST"])
def submitted_form():
    data.append("Name: " + request.form["name"])
    data.append("Url: " + request.form["url"])
    data.append("Duration: " + request.form["duration"])
    data.append("Concurrency: " + request.form["concurrency"])
    data.append("Threshold: " + request.form["threshold"])
    data.append("Peak: " + request.form["peak"])
    data.append("Dropdown: " + request.form["dropdown"])
    return render_template('index.html')


@app.errorhandler(500)
def server_error(_):
    # Log the error and stacktrace.
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500


def background_task():
    while len(data) == 0:
        time.sleep(1)

    for z in data:
        time.sleep(5)  # Simulate some work
        # Send message to client
        yield z


@app.route('/')
def start():
    return render_template('index.html')
    # return 'Hello world!', 200


# Route to stream updates to the client
@app.route('/stream')
def stream():
    return Response(background_task(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(port=8080)
