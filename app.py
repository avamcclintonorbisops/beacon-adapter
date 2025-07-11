from flask import Flask, request

app = Flask(__name__)
data = []

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def save_beacon():
    try:
        # Print raw body regardless of format
        raw_body = request.data.decode('utf-8', errors='replace')
        print("🔴 Raw Body:\n", raw_body)
        print("🔵 Headers:\n", dict(request.headers))

        # Try to parse as JSON
        content = request.get_json(force=True)
        print("✅ Parsed JSON:\n", content)

        if isinstance(content, list):
            data.extend(content)
        else:
            data.append(content)

        return {"status": "success"}, 200

    except Exception as e:
        print("❌ JSON parsing failed:", str(e))
        return {"error": "Invalid JSON", "details": str(e)}, 400

@app.route('/beacons')
def get_beacons():
    return {"data": data}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
