from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    data = request.get_json(silent=True)
    if not data:
        return '', 200  # Ignore bad JSON

    input1 = data.get("input1", [])
    input2 = data.get("input2", {})

    print("📡 input1:", input1)
    print("📍 input2:", input2)

    return '', 200  # Always return success

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
