from flask import Flask, request

app = Flask(__name__)
data = []

@app.route('/')
def home():
    return "Beacon Adapter is Live!"

@app.route('/beacon', methods=['POST'])
def save_beacon():
    if not request.is_json:
        return {"error": "Invalid JSON"}, 400
    data.append(request.get_json())
    return "OK"

@app.route('/beacons')
def get_beacons():
    return {"data": data}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
