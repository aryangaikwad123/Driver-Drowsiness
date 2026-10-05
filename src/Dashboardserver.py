from flask import Flask,jsonify,send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/dashboard-data")
def dashboard_data():

    with open("data.json") as f:
        data = json.load(f)

    return jsonify(data)

@app.route("/alert-image")
def alert_image():

    return send_from_directory(
        os.path.dirname(__file__),
        "alert.jpg"
    )

if __name__ == "__main__":
    app.run(debug=True)