from flask import Flask, render_template, jsonify
from shared_status import get_status

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html"
    )

@app.route("/api/status")
def status():
    return jsonify(get_status())

def run_dashboard():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )