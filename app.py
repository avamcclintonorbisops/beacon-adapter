from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)
data = []

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        # Fix invalid JSON: replace input2: N/A with input2: []
        raw = request.data.decode('utf-8')
        raw = re.sub(r'"input2"\s*:\s*N/A', '"input2": []', raw)

        payload = json.loads(raw)
        data.append(payload)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": "Invalid JSON", "details": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

