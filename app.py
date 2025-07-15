from flask import Flask, request, jsonify

app = Flask(__name__)
beacon_index = {}

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        # Print the raw request body for debugging
        raw_body = request.data.decode('utf-8', errors='replace')
        print("📦 Raw Payload:\n", raw_body)

        # Try to parse JSON
        payload = request.get_json(force=True)
        print("✅ Parsed JSON:\n", payload)

        # Process input1 (beacons)
        input_array = payload.get("input1", [])
        for item in input_array:
            name = item.get("name")
            if not name:
                continue
            # Replace existing entry
            beacon_index[name] = {
                k: v for k, v in item.items()
                if k not in ("data", "input1")
            }

        # Optionally print input2 if present
        if "input2" in payload:
            print("📍 GPS Data (input2):", payload["input2"])

        return jsonify({"status": "success", "index": beacon_index}), 200

    except Exception as e:
        print("❌ Error parsing request:", str(e))
        return jsonify({"error": "Bad Request", "details": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
