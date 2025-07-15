from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        # Try to parse JSON the standard way
        data = request.get_json(silent=True)

        if not data:
            # If that fails, decode raw body and parse manually
            raw_body = request.data.decode('utf-8')
            print("Raw (non-JSON) request:", raw_body)
            data = json.loads(raw_body)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        print("input1:", input1)
        print("input2:", input2)

    except Exception as e:
        print("Error:", e)

    return '', 200  # Always respond with 200 OK

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify({"message": "Not storing data in this version."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
