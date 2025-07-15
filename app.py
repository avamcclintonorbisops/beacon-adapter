from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

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

            # Fix malformed input2 with regex (replace double braces only around input2)
            raw_body = re.sub(r'"input2":\s*\{\{', '"input2":{', raw_body)
            raw_body = re.sub(r'\}\}\s*}$', '}}', raw_body)  # If extra braces are at the very end

            # Then attempt to parse cleaned data
            data = json.loads(raw_body)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        print("input1:", input1)
        print("input2:", input2)

        return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
