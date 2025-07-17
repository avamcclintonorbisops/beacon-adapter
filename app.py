from flask import Flask, request, jsonify
import json
from graphene import ObjectType, String, Field, Schema, Dict

app = Flask(__name__)

# Store most recent data per beacon
beacon_index = {}

@app.route('/')
def home():
    return "Beacon Adapter is running!"

@app.route('/beacons', methods=['POST'])
def handle_beacon():
    try:
        data = request.get_json(silent=True)

        if not data:
            raw_body = request.data.decode('utf-8')
            print("Raw (non-JSON) request:", raw_body)
            cleaned = raw_body.replace('input2":{{', 'input2":{').replace('}}}', '}}')
            data = json.loads(cleaned)

        input1 = data.get("input1", [])
        input2 = data.get("input2", {})

        for item in input1:
            name = item.get("name")
            if not name:
                continue
            beacon_index[name] = {
                "beacon": item,
                "gps": input2
            }

        print("input1:", input1)
        print("input2:", input2)

        return jsonify({"message": "Data stored successfully."}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/beacons', methods=['GET'])
def get_beacons():
    return jsonify(beacon_index)


# ---------------- GRAPHQL BELOW ---------------- #

class BeaconData(ObjectType):
    beacon = Dict()
    gps = Dict()

class Query(ObjectType):
    beacons = Field(Dict)
    beacon = Field(BeaconData, id=String(required=True))

    def resolve_beacons(root, info):
        return beacon_index

    def resolve_beacon(root, info, id):
        return beacon_index.get(id)

schema = Schema(query=Query)

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    query = data.get("query")

    result = schema.execute(query)
    return jsonify({
        "data": result.data,
        "errors": [str(e) for e in result.errors] if result.errors else None
    })

# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
