import json
import re
from flask import Flask, request

app = Flask(__name__)

# Store received beacon data
data_store = []

@app.route("/beacon", methods=["POST"])
def receive_data():
    try:
        # Step 1: Decode raw bytes to text
        raw = request.data.decode("utf-8")


        # Step 3: Parse JSON
        parsed = json.loads(cleaned)

        # Step 4: Store and print
        data_store.append(parsed)
        print("✅ Received payload:")
        print(json.dumps(parsed, indent=2))

        return "OK", 200
    except Exception as e:
        print("❌ Error parsing request:", e)
        return "Error", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
