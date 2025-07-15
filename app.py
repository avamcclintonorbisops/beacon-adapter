from flask import Flask, request, jsonify

app = Flask(__name__)

# Store most recent beacon data (indexed by name)
beacon_index = {}

@app.route('/')

@@ -13,27 +11,34 @@ def home():
def handle_beacon():
    try:
        payload = request.get_json(force=True)
        input_array = payload.get("input1", [])

        for item in input_array:
        # Print for debugging
        print("📩 Payload:", payload)

        input1 = payload.get("input1", [])
        input2 = payload.get("input2", {})  # GPS data is here

        for item in input1:
            name = item.get("name")
            if not name:
                continue

            # Remove old entry
            beacon_index.pop(name, None)

            # Filter out 'data' and 'input1'
            # Replace old data with the latest reading
            filtered_item = {
                k: v for k, v in item.items()
                if k not in ("data", "input1")
            }

            # Attach latest GPS data if available
            if input2:
                filtered_item["gps"] = input2

            beacon_index[name] = filtered_item

        return jsonify({"status": "success", "current_index": beacon_index}), 200
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"status": "error", "details": str(e)}), 400

@app.route('/beacons', methods=['GET'])