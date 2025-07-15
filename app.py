from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Simple index route
@app.route('/')
def home():
    return "Beacon Adapter is running!"

# Endpoint for receiving beacon data
@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        # Try to parse standard JSON payload
        data = request.get_json(silent=True)

        if not data:
            # Fallback: handle non-JSON-encoded body
            raw_body = request.data.decode('utf-8')
            print("Raw (non-JSON) request:", raw_body)

            # Fix malformed input2 payload
            cleaned = raw_body.replace('input2":{{', 'input2":{').replace('}}}', '}')

            data = json.loads(cleaned)

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
