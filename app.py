from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/beacon", methods=["POST"])
def receive_beacon_data():
    try:
        data = request.get_json()
        print("📦 Received JSON:")
        print(data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print("❌ Error parsing request:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
