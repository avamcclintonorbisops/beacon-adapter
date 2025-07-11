from flask import Flask, request

app = Flask(__name__)
data = []

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def save_beacon():
    try:
        if not request.is_json:
            return {"error": "Request is not JSON", "content_type": request.content_type}, 400

        content = request.get_json(force=True)  # force=True to try parsing anyway

        print("🔵 Headers:", dict(request.headers))
        print("📦 Payload:", content)

        if isinstance(content, list):
            data.extend(content)
        else:
            data.append(content)

        return {"status": "success"}, 200

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return {"error": str(e)}, 400

@app.route('/beacons')
def get_beacons():
    return {"data": data}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
