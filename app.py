import logging
import time
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/submitted", methods=["POST"])
def submitted_form():
    name = request.form["name"]
    email = request.form["email"]
    site = request.form["site_url"]
    comments = request.form["comments"]

    return render_template(
        "submitted_form.html", name=name, email=email, site=site, comments=comments
    )


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500


def background_task():
    for i in range(10):
        time.sleep(1)  # Simulate some work
        # Send message to client
        yield f"data: Task update {i+1}\n\n"


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
