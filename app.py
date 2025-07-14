from flask import Flask, request, jsonify

app = Flask(__name__)

# Store most recent beacon data (indexed by name)
beacon_index = {}

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        payload = request.get_json(force=True)
        input_array = payload.get("input1", [])

        for item in input_array:
            name = item.get("name")
            if not name:
                continue

            # Remove old entry
            beacon_index.pop(name, None)

            # Filter out 'data' and 'input1'
            filtered_item = {
                k: v for k, v in item.items()
                if k not in ("data", "input1")
            }

            beacon_index[name] = filtered_item

        return jsonify({"status": "success", "current_index": beacon_index}), 200

    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
