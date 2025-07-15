from flask import Flask, request

app = Flask(__name__)

@app.route("/beacon", methods=["POST"])
def receive_data():
    data = request.data
    print("📦 Raw Payload:\n", data)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

