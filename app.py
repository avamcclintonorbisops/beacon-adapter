from flask import Flask, request, jsonify

app = Flask(__name__)
beacon_index = {}

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        payload = request.get_json(force=True)

        input1_array = payload.get("input1", [])
        input2_array = payload.get("input2", [])

        if not isinstance(input1_array, list):
            return jsonify({"error": "input1 is not a list"}), 400

        if not isinstance(input2_array, list):
            input2_array = []  # Ignore input2 if it's not a valid list (e.g., N/A string)

        # Process input1
        for item in input1_array:
            name = item.get("name")
            if not name:
                continue
            beacon_index.pop(name, None)
            filtered_item = {
                k: v for k, v in item.items()
                if k not in ("data", "input1")
            }
            beacon_index[name] = filtered_item

        # Process input2
        for item in input2_array:
            name = item.get("name", "unknown_input2")
            key = f"input2_{name}"
            beacon_index.pop(key, None)
            filtered_item = {
                k: v for k, v in item.items()
                if k not in ("data", "input1")
            }
            beacon_index[key] = filtered_item

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": "Invalid JSON", "details": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
