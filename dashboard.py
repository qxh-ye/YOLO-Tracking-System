from flask import Flask, render_template, jsonify

app = Flask(__name__)

data = {
    "fps": 15.6,
    "roi_count": 3,
    "enter_count": 5,
    "exit_count": 2,
    "events": [
        "ID 1 ROI ENTER",
        "ID 3 LINE ENTER"
    ]
}

@app.route("/")
def index():
    return render_template(
        "index.html",
        data=data
    )

@app.route("/api/status")
def status():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)