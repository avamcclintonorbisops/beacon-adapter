from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    data = request.get_json(silent=True)

    print("Payload:", data)

    if not data:
        print("Raw (non-JSON) request:", request.data)
        return '', 200  # Avoid crashing on bad input

    input1 = data.get("input1", [])
    input2 = data.get("input2", {})

    print("input1:", input1)
    print("input2:", input2)

    return '', 200  # Return success always

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify({"message": "Not storing data in this version."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
