from flask import Flask, request, jsonify

app = Flask(__name__)
beacon_index = {}

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    payload = request.get_json(force=True)
    input_array = payload.get("input1", [])

    for item in input_array:
        name = item.get("name")
        if not name:
            continue

        # Remove any existing entry for this beacon
        beacon_index.pop(name, None)

        # Filter out unwanted fields
        filtered_item = {
            k: v for k, v in item.items()
            if k not in ("data", "input1")
        }

        beacon_index[name] = filtered_item

    return jsonify({"status": "success"}), 200

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
