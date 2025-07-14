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

        # Print for debugging
        print("📩 Payload:", payload)

        input1 = payload.get("input1", [])
        input2 = payload.get("input2", {})  # GPS data is here

        for item in input1:
            name = item.get("name")
            if not name:
                continue

            # Replace old data with the latest reading
            filtered_item = {
                k: v for k, v in item.items()
                if k not in ("data", "input1")
            }

            # Attach latest GPS data if available
            if input2:
                filtered_item["gps"] = input2

            beacon_index[name] = filtered_item

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"status": "error", "details": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
