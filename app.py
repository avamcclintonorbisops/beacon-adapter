from flask import Flask, request, jsonify
import time

app = Flask(__name__)

last_update_time = 0
latest_input1 = None
latest_input2 = None

@app.route("/beacon", methods=["POST"])
def receive_beacon_data():
    global last_update_time, latest_input1, latest_input2

    try:
        data = request.get_json()

        # Update only if 10 seconds have passed
        if time.time() - last_update_time > 10:
            latest_input1 = data.get("input1", None)
            latest_input2 = data.get("input2", None)
            last_update_time = time.time()

            print("\n🔁 Updated Data:")
            print("input1:", latest_input1)
            print("input2:", latest_input2)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("❌ Error parsing request:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
