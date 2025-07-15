from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

# Store beacons here
data_store = []

@app.route("/beacon", methods=["POST"])
def receive_data():
    try:
        # Preprocess: Replace "N/A" with null to make valid JSON
        raw = request.data.decode("utf-8")
        cleaned = re.sub(r'"input2"\s*:\s*N/A', '"input2": null', raw)

        parsed = json.loads(cleaned)
        data_store.append(parsed)
        return "OK", 200
    except Exception as e:
        print("❌ Error parsing request:", e)
        return "Bad Request", 400

@app.route("/beacons", methods=["GET"])
def get_data():
    return jsonify(data_store)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
