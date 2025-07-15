from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Store most recent data for each beacon
beacon_index = {}

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacons', methods=['POST'])
def handle_beacon():
    try:
        data = request.get_json(silent=True)

        if not data:
            raw_body = request.data.decode('utf-8')
            print("Raw (non-JSON) request:", raw_body)
            cleaned = raw_body.replace('input2': '{{', 'input2': '{').replace('}}}', '}}')
            data = json.loads(cleaned)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        for item in input1:
            name = item.get("name")
            if not name:
                continue

            # Store most recent data per beacon
            beacon_index[name] = {
                "beacon": item,
                "gps": input2
            }

        print("input1:", input1)
        print("input2:", input2)

        return jsonify({"message": "Data stored successfully."}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index)
