from flask import Flask, request, jsonify

app = Flask(__name__)

# beacon_index is now a list so we can append to it
beacon_index = []

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    data = request.get_json(silent=True)
    if not data:
        return '', 200  # Don't crash on bad JSON

    input1 = data.get("input1", [])
    input2 = data.get("input2", [])

    # Fix: append to list, not dict
   beacon_index = request.get_json()

    print(beacon_index)
    return '', 200  # Always return 200 OK

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
