from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacon', methods=['POST'])
def handle_beacon():
    try:
        data = request.get_json(silent=True)
        print("Payload:", data)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        print("input1:", input1)
        print("input2:", input2)

        return '', 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "details": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
